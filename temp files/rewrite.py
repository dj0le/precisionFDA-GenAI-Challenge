import pymupdf4llm
from typing import List
from langchain_core.documents import Document

def process_pdf(file_path: str) -> List[Document]:
    pdf_data = pymupdf4llm.to_markdown(file_path, page_chunks=True)

    documents = []

    for page in pdf_data:
        # remove None and non-primitive types
        clean_metadata = {
            k: v for k, v in page["metadata"].items()
            if v is not None and isinstance(v, (str, int, float, bool))
        }

        # Get title, or set metadata title if field is empty
        source = clean_metadata.get("title")
        if not source:
            file_path = clean_metadata.get("file_path", "")
            filename = file_path.split('/')[-1].split('\\')[-1]
            filename = filename.rsplit('.', 1)[0]
            clean_metadata["title"] = filename
            source = filename

        # Truncate filename
        if len(source) > 55:
            source = source[:52] + "..."

        page_num = clean_metadata.get("page")
        page_id = f"{source}:{page_num}"
        clean_metadata["id"] = page_id

        # Return Langchain Document
        doc = Document(
            page_content=page["text"],
            metadata=clean_metadata
        )
        documents.append(doc)

    return documents






def populate_vectordb(data: dict):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=process_embeddings()
    )

    # Add or Update the documents
    db_items = db.get(include=[])
    db_ids = set(db_items["ids"])
    print(f"Number of existing documents in DB: {len(db_ids)}")

    # Prepare new documents for addition
    new_documents = []
    new_ids = []
    new_metadatas = []

    for page in data:
        page_id = page["metadata"]["id"]
        if page_id not in db_ids:
            cleaned_metadata = {
                k: v for k, v in page["metadata"].items()
                if v is not None and isinstance(v, (str, int, float, bool))
            }

            new_documents.append(page["text"])
            new_ids.append(page_id)
            new_metadatas.append(cleaned_metadata)

    if new_documents:
        print(f"👉 Adding new documents: {len(new_documents)}")
        db.add_texts(
            texts=new_documents,
            ids=new_ids,
            metadatas=new_metadatas
        )

        print("✅ Documents added successfully")
    else:
        print("✅ No new documents to add")

    return db
