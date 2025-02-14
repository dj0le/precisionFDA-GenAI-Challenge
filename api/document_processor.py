import os
from fastapi import HTTPException
from typing import List, Dict, Any
from utils.chroma_manager import ChromaManager

class DocumentProcessor:
    def __init__(self, chroma_path: str, embedding_function):
        self._chroma_path = chroma_path
        self._embedding_function = embedding_function
        self._db_manager = ChromaManager()
        self._db_manager.initialize(chroma_path, embedding_function)

    def populate_vectordb(self, data: List[Dict[str, Any]], file_id: str) -> None:
        try:
            db_items = self._db_manager.get_all_documents(include=[])
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
                self._db_manager.add_documents(new_documents, new_ids, new_metadatas)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to populate vector database: {str(e)}"
            )

    def delete_doc_from_chroma(self, file_id: str, embedding_function: Any) -> bool:
        """Delete a document from ChromaDB by file ID."""
        try:
            return self._db_manager.delete_documents(file_id, self._chroma_path, embedding_function)
        except Exception as e:
            print(f"Error deleting document from Chroma: {e}")
            return False
