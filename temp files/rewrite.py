import pymupdf4llm
from langchain_core.documents import Document
from typing import List


def process_pdf(file_path):
    pdf_data = pymupdf4llm.to_markdown(file_path, page_chunks=True)

    for page in pdf_data:
        # Get title, or set metadata title if field is empty
        source = page["metadata"].get("title")
        if not source:
            file_path = page["metadata"].get("file_path", "")
            filename = file_path.split('/')[-1].split('\\')[-1]
            filename = filename.rsplit('.', 1)[0]
            page["metadata"]["title"] = filename
            source = filename

        page_num = page["metadata"].get("page")
        page_id = f"{source}:{page_num}"
        page["metadata"]["id"] = page_id

    return pdf_data



==========

    print(json.dumps(data[0]["metadata"], indent=4))
    populate_vectordb(data)



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
