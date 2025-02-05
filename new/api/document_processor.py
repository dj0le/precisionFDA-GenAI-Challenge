import hashlib
from fastapi import HTTPException
from langchain_chroma import Chroma
from typing import List, Dict, Any

class DocumentProcessor:
    def __init__(self, chroma_path: str, embedding_function):
        self._chroma_path = chroma_path
        self._embedding_function = embedding_function
        try:
            self._db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize Chroma database: {str(e)}"
            )

    @staticmethod
    def get_file_hash(contents: bytes) -> str:
        return hashlib.sha256(contents).hexdigest()

    def populate_vectordb(self, data: List[Dict[str, Any]], file_id: int) -> None:
        try:
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

    def delete_doc_from_chroma(self, file_id: int) -> bool:
        try:
            self._db._collection.delete(where={"file_id": file_id})
            return True

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete document with file_id {file_id} from Chroma: {str(e)}"
            )
