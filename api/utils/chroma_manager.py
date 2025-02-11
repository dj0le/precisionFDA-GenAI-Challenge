import os
import shutil
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from langchain_chroma import Chroma

class ChromaManager:
    _instance: Optional['ChromaManager'] = None
    _db: Optional[Chroma] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaManager, cls).__new__(cls)
        return cls._instance

    def initialize(self, chroma_path: str, embedding_function: Any):
        """Initialize or reinitialize the database"""
        try:
            os.makedirs(chroma_path, exist_ok=True)
            self._db = Chroma(
                persist_directory=chroma_path,
                embedding_function=embedding_function,
                collection_name="documents"
            )
            print(f"Initialized Chroma DB at {chroma_path}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize Chroma database: {str(e)}"
            )

    @property
    def db(self) -> Chroma:
        if self._db is None:
            raise HTTPException(
                status_code=500,
                detail="Chroma database not initialized"
            )
        return self._db

    def reset_db(self, chroma_path: str):
        """Reset the database by removing and recreating it"""
        try:
            if os.path.exists(chroma_path):
                print("No documents remain in database, resetting...")
                shutil.rmtree(chroma_path)
                self.initialize(chroma_path, self._db._embedding_function)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to reset database: {str(e)}"
            )

    def add_documents(self, texts: List[str], ids: List[str], metadatas: List[Dict]):
        """Add documents to the database"""
        self.db.add_texts(texts=texts, ids=ids, metadatas=metadatas)

    def delete_documents(self, file_id: str, chroma_path: str) -> bool:
        """Delete documents by file_id"""
        try:
            matching_docs = self.db._collection.get(where={"file_id": file_id})
            print(f"Found {len(matching_docs['ids'])} documents to delete")

            self.db._collection.delete(where={"file_id": file_id})

            remaining_docs = self.db._collection.get(where={"file_id": file_id})
            if remaining_docs['ids']:
                print(f"Warning: {len(remaining_docs['ids'])} documents still remain")

            # Check if database is empty
            all_docs = self.db.get(include=[])
            if not all_docs["ids"]:
                self.reset_db(chroma_path)

            return True
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete documents: {str(e)}"
            )

    def search_documents(self, query: str, k: int = 3):
        """Search for relevant documents"""
        return self.db.similarity_search_with_score(query, k=k)

    def get_all_documents(self, include: List = None):
        """Get all documents"""
        return self.db.get(include=include or [])
