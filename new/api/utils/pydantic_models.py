from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from utils.model_utils import get_available_models

class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = Field(default=None)
    model: str = Field(default="llama3.2")
    filename: Optional[str] = None

    @validator('model')
    def validate_model(cls, v):
        available_models = get_available_models()
        if v not in available_models:
            raise ValueError(f"Model must be one of: {available_models}")
        return v

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]  # Document IDs used as sources
    response_metadata: Dict[str, Any]  # For flexible metadata structure
    usage_metadata: Dict[str, Any]  # For flexible metadata structure
    session_id: str
    model: str
    filename: Optional[str] = None

class DocumentMetadata(BaseModel):
    file_id: int  # metadata sqltable row
    file_hash: str  # SHA-256 hash
    filename: str
    upload_timestamp: datetime

    class Config:
        from_attributes = True

class DeleteFileRequest(BaseModel):
    file_id: int
