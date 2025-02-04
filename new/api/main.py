import os, uuid, shutil
from config import settings
from fastapi import FastAPI, File, UploadFile, HTTPException
from document_processor import DocumentProcessor
from utils.db_utils import get_all_documents, insert_document_record, delete_document_record
from utils.pdf_utils import process_pdf
from utils.model_utils import process_embeddings, get_available_models
from utils.pydantic_models import DocumentMetadata, DeleteFileRequest

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "precisionFDA Gen AI Challenge future landing page"}

@app.get("/available-models")
def get_models():
    return {"models": get_available_models()}

@app.post("/upload-doc")
async def process_document(
    file: UploadFile):
    try:
        # Validate file size before reading
        file_size = 0
        while chunk := await file.read(8192):
            file_size += len(chunk)
            if file_size > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE/1_000_000:.1f}MB"
                )

        # Reset file pointer
        await file.seek(0)

        # Validate filename and extension
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")

        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types are: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )

        # Create temp directory if it doesn't exist
        os.makedirs(settings.TEMP_UPLOAD_DIR, exist_ok=True)
        temp_file_path = os.path.join(settings.TEMP_UPLOAD_DIR, f"{uuid.uuid4()}{file_extension}")

        try:
            # Save file to temp location
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Process the file
            contents = await file.read()
            file_hash = DocumentProcessor.get_file_hash(contents)

            try:
                file_id = insert_document_record(file.filename, file_hash)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

            data = process_pdf(temp_file_path, file_id, file_hash)
            doc_processor = DocumentProcessor(settings.CHROMA_PATH, process_embeddings())
            doc_processor.populate_vectordb(data, file_id)

            return {
                "message": f"File {file.filename} has been successfully uploaded and indexed.",
                "file_id": file_id
            }

        finally:
            # Cleanup temp file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    except Exception as e:
        # Cleanup on failure
        if 'file_id' in locals():
            delete_document_record(file_id)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-docs", response_model=list[DocumentMetadata])
async def list_documents():
    try:
        return get_all_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    # delete from the llm vector db
    doc_processor = DocumentProcessor(settings.CHROMA_PATH, process_embeddings())
    chroma_delete_success = doc_processor.delete_doc_from_chroma(request.file_id)

    # Delete Metadata from database
    if chroma_delete_success:
        db_delete_success = delete_document_record(request.file_id)
        if db_delete_success:
            return {"message": f"Successfully deleted document {request.file_id}"}
        else:
            return {"error": f"Deleted from Chroma but failed to delete {request.file_id} from database"}
    else:
        return {"error": f"Failed to delete document {request.file_id} from Chroma"}
