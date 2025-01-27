from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime

class ModelName(str, Enum):
    @classmethod
    def _missing_(cls, value):
        # This allows the Enum to accept any string value
        return value

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=None)

    class Config:
        arbitrary_types_allowed = True

    @validator('model', pre=True, always=True)
    def set_default_model(cls, v):
        if v is None:
            # You could also fetch this from a config or environment variable
            return "llama2"  # default model
        return v

# class QueryInput(BaseModel):
#     question: str
#     session_id: str = Field(default=None)
#     model: ModelName = Field(default="llama3.2")


class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int
