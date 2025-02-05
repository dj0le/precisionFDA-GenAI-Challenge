import ollama
from datetime import datetime
from pydantic import BaseModel, Field, validator
from config import settings

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: str = Field(default=settings.DEFAULT_MODEL)

    @validator('model')
    def validate_model(cls, v):
        if v not in settings.AVAILABLE_MODELS:
            raise ValueError(f"Model must be one of: {settings.AVAILABLE_MODELS}")
        return v

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: str

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int
