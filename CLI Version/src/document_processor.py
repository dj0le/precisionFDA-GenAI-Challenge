from langchain_chroma import Chroma
from typing import List, Dict, Any

class DocumentProcessor:
    def __init__(self, chroma_path: str, embedding_function):
        self._chroma_path = chroma_path
        self._embedding_function = embedding_function
        self._db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

    def populate_vectordb(self, data: List[Dict[str, Any]]) -> None:
        db_items = self._db.get(include=[])
        db_ids = set(db_items["ids"])
        print(f"Number of existing documents in DB: {len(db_ids)}")

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
            self._db.add_texts(
                texts=new_documents,
                ids=new_ids,
                metadatas=new_metadatas
            )
            print("✅ Documents added successfully")
        else:
            print("✅ No new documents to add")
