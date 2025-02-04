import ollama
from datetime import datetime
from pydantic import BaseModel, Field, validator

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: str = Field(default="llama3.2")

    @validator('model')
    def validate_model(cls, v):
        available_models = get_available_models()
        if v not in available_models:
            raise ValueError(f"Model must be one of: {available_models}")
        return v

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: str

class DocumentMetadata(BaseModel):
    file_id: int  # metadata sqltable row
    file_hash: str  # SHA-256 hash
    filename: str
    upload_timestamp: datetime

    class Config:
        from_attributes = True

class DeleteFileRequest(BaseModel):
    file_id: int
