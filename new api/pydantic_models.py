import ollama
from datetime import datetime
from pydantic import BaseModel, Field, validator

def get_available_models():
    try:
        model_list = ollama.list()
        return [model_info['model'].split(':')[0] for model_info in model_list['models']]
    except Exception:
        return ['llama3.2']

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

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int
