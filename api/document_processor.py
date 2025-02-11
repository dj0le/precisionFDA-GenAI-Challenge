import os
import shutil
from fastapi import HTTPException
from langchain_chroma import Chroma
from typing import List, Dict, Any

class DocumentProcessor:
    def __init__(self, chroma_path: str, embedding_function):
        self._chroma_path = chroma_path
        self._embedding_function = embedding_function
        self._initialize_db()

    def _initialize_db(self):
        """Initialize or reinitialize the Chroma database"""
        try:
            os.makedirs(self._chroma_path, exist_ok=True)
            self._db = Chroma(
                persist_directory=self._chroma_path,
                embedding_function=self._embedding_function,
                collection_name="documents"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize Chroma database: {str(e)}"
            )

    def populate_vectordb(self, data: List[Dict[str, Any]], file_id: str) -> None:
        try:
            if not hasattr(self, '_db'):
                self._initialize_db()

            db_items = self._db.get(include=[])
            db_ids = set(db_items["ids"])

            new_documents = []
            new_ids = []
            new_metadatas = []

            for page in data:
                page_id = f"{file_id}_{page['metadata']['page']}"
                if page_id not in db_ids:
                    cleaned_metadata = {
                        k: v for k, v in page["metadata"].items()
                        if v is not None and isinstance(v, (str, int, float, bool))
                    }
                    cleaned_metadata["file_id"] = file_id

                    source_filename = page["metadata"].get("source", "")
                    truncated_filename = os.path.splitext(source_filename)[0][:45]

                    cleaned_metadata["original_filename"] = (
                        page["metadata"].get("title") or
                        truncated_filename or
                        "Unknown"
                    )
                    cleaned_metadata["page_number"] = page["metadata"].get("page", 0)

                    new_documents.append(page["text"])
                    new_ids.append(page_id)
                    new_metadatas.append(cleaned_metadata)

            if new_documents:
                self._db.add_texts(texts=new_documents, ids=new_ids, metadatas=new_metadatas)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to populate vector database: {str(e)}"
            )

    def delete_doc_from_chroma(self, file_id: str) -> bool:
            try:
                matching_docs = self._db._collection.get(where={"file_id": file_id})
                print(f"Found {len(matching_docs['ids'])} documents to delete")

                self._db._collection.delete(where={"file_id": file_id})

                remaining_docs = self._db._collection.get(where={"file_id": file_id})
                if remaining_docs['ids']:
                    print(f"Warning: {len(remaining_docs['ids'])} documents still remain")

                all_docs = self._db.get(include=[])
                if not all_docs["ids"]:
                    if os.path.exists(self._chroma_path):
                        shutil.rmtree(self._chroma_path)
                    self._initialize_db()

                return True
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to delete document with file_id {file_id} from Chroma: {str(e)}"
                )
