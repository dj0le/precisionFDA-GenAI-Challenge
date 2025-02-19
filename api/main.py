import csv
import io
import os
import shutil
import tempfile
import uuid
from typing import List

# Third-party imports
from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

# Local application imports
from config import settings
from document_processor import DocumentProcessor
from llm_engine import LLMQueryEngine
from results_processor import BatchResultsProcessor
from chat_engine import ChatEngine
from utils.db_utils import (
    get_all_documents,
    insert_document_record,
    delete_document_record,
    get_chat_history,
    insert_chat_history
)
from utils.hash_utils import get_file_hash
from utils.model_utils import process_embeddings, get_available_models
from utils.pdf_utils import process_pdf
from utils.pydantic_models import (
    BatchQueryResponse,
    BatchSummary,
    DeleteFileRequest,
    DocumentMetadata,
    OutputFormat,
    QueryInput,
    QueryResponse,
    QuestionResponse,
)

app = FastAPI()

origins = [
    "http://localhost:5173",  # Add your Svelte dev server port
    "http://localhost:4173",  # Add your Svelte preview port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "models_loaded": get_available_models()
    }

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id or str(uuid.uuid4())

    chat_history = get_chat_history(session_id)

    chat_engine = ChatEngine(model=query_input.model)
    result = chat_engine.get_response(query_input.question, chat_history)

    processing_time = result["response_metadata"].get("total_duration", 0)
    tokens = result["usage_metadata"].get("total_tokens", 0)

    insert_chat_history(
        session_id=session_id,
        user_query=query_input.question,
        llm_response=result["response"],
        sources=",".join(result["sources"]),
        processing_time=processing_time,
        tokens=tokens
    )

    return QueryResponse(
        answer=result["response"],
        sources=result["sources"],
        response_metadata=result["response_metadata"],
        usage_metadata=result["usage_metadata"],
        session_id=session_id,
        model=query_input.model,
        filename=query_input.filename
    )

@app.post("/upload-doc")
async def process_document(file: UploadFile):
    file_id = None
    try:
        contents = await file.read()
        file_size = len(contents)

        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE/1_000_000:.1f}MB"
            )

        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")

        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types are: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )

        file_hash = get_file_hash(contents)

        try:
            file_id = insert_document_record(file.filename, file_hash)
            if file_id is None:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to generate file ID"
                )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Save to temp file for processing
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name

            try:
                data = process_pdf(temp_file_path, file_id, file_hash, original_filename=file.filename)
                # Explicitly initialize ChromaManager with the embedding function
                embedding_function = process_embeddings()
                doc_processor = DocumentProcessor(settings.CHROMA_PATH, embedding_function)
                doc_processor.populate_vectordb(data, file_id)

                return {
                    "message": f"File {file.filename} has been successfully uploaded and indexed.",
                    "file_id": file_id
                }

            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

    except Exception as e:
        # Cleanup on failure
        if file_id:
            delete_document_record(file_id)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query-documents", response_model=QueryResponse)
async def query_documents(query_input: QueryInput):
    try:
        # Initialize LLM engine with current settings
        llm_engine = LLMQueryEngine(
            settings.CHROMA_PATH,
            process_embeddings(),
            query_input.model
        )

        # Process query
        query_result = llm_engine.query(query_input.question)

        # Construct response
        response = QueryResponse(
            answer=query_result["response"],
            sources=query_result["sources"],
            response_metadata=query_result["response_metadata"],
            usage_metadata=query_result["usage_metadata"],
            session_id=query_input.session_id,
            model=query_input.model,
            filename=query_input.filename
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.get("/list-docs", response_model=list[DocumentMetadata])
async def list_documents():
    try:
        documents = get_all_documents()

        # If metadata database is empty, clear Chroma
        if not documents:
            if os.path.exists(settings.CHROMA_PATH):
                shutil.rmtree(settings.CHROMA_PATH)
                print("Cleared Chroma directory due to empty metadata database")

        return documents

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    # delete from the llm vector db
    embedding_function = process_embeddings()  # Get the embedding function
    doc_processor = DocumentProcessor(settings.CHROMA_PATH, embedding_function)
    chroma_delete_success = doc_processor.delete_doc_from_chroma(request.file_id, embedding_function=embedding_function)

    # Delete Metadata from database
    if chroma_delete_success:
        db_delete_success = delete_document_record(request.file_id)
        if db_delete_success:
            return {"message": f"Successfully deleted document {request.file_id}"}
        else:
            return {"error": f"Deleted from Chroma but failed to delete {request.file_id} from database"}
    else:
        return {"error": f"Failed to delete document {request.file_id} from Chroma"}

# submit questions from a file
@app.post("/batch-query/upload", response_model=BatchQueryResponse)
async def batch_query_upload(
    file: UploadFile = File(...),
    model: str = "llama3.2",
    output_format: OutputFormat = OutputFormat.JSON
):
    try:
        # Read and validate CSV file
        content = await file.read()
        text_content = content.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(text_content))
        questions = [row[0] for row in csv_reader if row]  # Assuming one question per row

        # Process questions
        processor = BatchResultsProcessor(model_name=model)
        llm_engine = LLMQueryEngine(
            settings.CHROMA_PATH,
            process_embeddings(),
            model
        )

        for question in questions:
            result = llm_engine.query(question)
            processor.add_result(question, result)

        # Get formatted results
        results = processor.get_formatted_results()

        # Handle different output formats
        if output_format == OutputFormat.TEXT:
            text_output = processor.to_text()
            return Response(
                content=text_output,
                media_type="text/plain",
                headers={
                    "Content-Disposition": f"attachment; filename=batch_results.txt"
                }
            )
        else:  # JSON format
            return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing batch query: {str(e)}"
        )

# submit questions directly as a JSON array in the request body
@app.post("/batch-query/list", response_model=BatchQueryResponse)
async def batch_query_list(
    questions: List[str],
    model: str = "llama3.2",
    output_format: OutputFormat = OutputFormat.JSON
):
    try:
        processor = BatchResultsProcessor(model_name=model)
        llm_engine = LLMQueryEngine(
            settings.CHROMA_PATH,
            process_embeddings(),
            model
        )

        for question in questions:
            result = llm_engine.query(question)
            processor.add_result(question, result)

        results = processor.get_formatted_results()

        if output_format == OutputFormat.TEXT:
            text_output = processor.to_text()
            return Response(
                content=text_output,
                media_type="text/plain",
                headers={
                    "Content-Disposition": f"attachment; filename=batch_results.txt"
                }
            )
        else:  # JSON format
            return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing batch query: {str(e)}"
        )
