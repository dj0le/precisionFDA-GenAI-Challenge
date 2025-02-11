from typing import List, Optional, Dict, Any
from datetime import datetime
from utils.formatting import format_duration
from pydantic import BaseModel, Field, validator
from utils.model_utils import get_available_models
from enum import Enum

class QueryInput(BaseModel):
    question: str
    session_id: str
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
    sources: List[str]
    response_metadata: Dict[str, Any]
    usage_metadata: Dict[str, Any]
    session_id: str
    model: str
    filename: Optional[str] = None

    @property
    def formatted_processing_time(self) -> str:
        """Returns human-readable processing time"""
        duration = self.response_metadata.get("total_duration", 0)
        return format_duration(duration)

    @property
    def total_tokens(self) -> int:
        """Returns total tokens used"""
        return self.usage_metadata.get("total_tokens", 0)

class DocumentMetadata(BaseModel):
    file_id: str  # metadata sqltable row
    file_hash: str  # SHA-256 hash
    filename: str
    upload_timestamp: datetime

    class Config:
        from_attributes = True

class DeleteFileRequest(BaseModel):
    file_id: str

class OutputFormat(str, Enum):
    TEXT = "text"
    JSON = "json"
    BOTH = "both"

class BatchQueryQuestion(BaseModel):
    question: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class QuestionResponse(BaseModel):
    question_number: int
    question: str
    answer: str
    sources: List[str]
    processing_time_ns: int
    total_tokens: int
    metadata: Dict[str, Any]

class BatchSummary(BaseModel):
    timestamp: str
    model: str
    question_count: int
    total_processing_time_ns: int
    avg_processing_time_ns: float
    total_tokens: int
    avg_tokens_per_question: float

class BatchQueryResponse(BaseModel):
    summary: BatchSummary
    responses: List[QuestionResponse]
