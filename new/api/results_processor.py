from enum import Enum
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
import json
from datetime import datetime
from src.config_utils import format_timestamp, format_duration

class OutputFormat(Enum):
    TEXT = "text"
    JSON = "json"
    BOTH = "both"

class QuestionResponse(BaseModel):
    question_number: int = Field(description="The sequential number of the question")
    question: str = Field(description="The question that was asked")
    answer: str = Field(description="The answer provided by the LLM")
    sources: List[str] = Field(description="List of source documents used")
    processing_time_ns: int = Field(description="Processing time in nanoseconds")
    total_tokens: int = Field(description="Total tokens used for this question")

class TestRunSummary(BaseModel):
    date: str = Field(description="Date and time of the test run")
    model: str = Field(description="Name of the LLM model used")
    question_count: int = Field(description="Total number of questions processed")
    total_processing_time_ns: int = Field(description="Total processing time in nanoseconds")
    avg_processing_time_ns: float = Field(description="Average processing time per question")
    total_tokens: int = Field(description="Total tokens used in the entire run")
    avg_tokens_per_question: float = Field(description="Average tokens used per question")

class TestRunResult(BaseModel):
    summary: TestRunSummary = Field(description="Summary of the entire test run")
    responses: List[QuestionResponse] = Field(description="List of individual question responses")

class ResultsProcessor:
    def __init__(self, base_output_file: str, output_format: OutputFormat = OutputFormat.BOTH):
        self.base_output_file = base_output_file
        self.output_format = output_format
        self.results = []
        self.metadata = {
            "total_duration": 0,
            "total_tokens": 0,
            "first_timestamp": None,
            "model_name": None,
            "question_count": 0
        }

    @property
    def text_output_file(self) -> str:
        return f"{self.base_output_file}.txt"

    @property
    def json_output_file(self) -> str:
        return f"{self.base_output_file}.json"

    def add_result(self, question: str, result: dict):
        self.results.append((question, result))
        self._update_metadata(result)
        self.metadata["question_count"] += 1

    def _update_metadata(self, result: dict):
        self.metadata["total_duration"] += result['response_metadata']['total_duration']
        self.metadata["total_tokens"] += result['usage_metadata']['total_tokens']
        if not self.metadata["first_timestamp"]:
            self.metadata["first_timestamp"] = result['response_metadata']['created_at']
        if not self.metadata["model_name"]:
            self.metadata["model_name"] = result['response_metadata']['model']

    def _create_summary(self) -> TestRunSummary:
        return TestRunSummary(
            date=self.metadata["first_timestamp"],
            model=self.metadata["model_name"],
            question_count=self.metadata["question_count"],
            total_processing_time_ns=self.metadata["total_duration"],
            avg_processing_time_ns=self.metadata["total_duration"] / self.metadata["question_count"],
            total_tokens=self.metadata["total_tokens"],
            avg_tokens_per_question=self.metadata["total_tokens"] / self.metadata["question_count"]
        )

    def _create_responses(self) -> List[QuestionResponse]:
        responses = []
        for i, (question, result) in enumerate(self.results, 1):
            response = QuestionResponse(
                question_number=i,
                question=question,
                answer=result["response"],
                sources=result["sources"],
                processing_time_ns=result["response_metadata"]["total_duration"],
                total_tokens=result["usage_metadata"]["total_tokens"]
            )
            responses.append(response)
        return responses

    def _write_text_results(self):
        with open(self.text_output_file, "w") as f:
            self._write_summary(f)
            self._write_questions(f)
        print(f"✅ Text results saved to {self.text_output_file}")

    def _write_json_results(self):
        test_run = TestRunResult(
            summary=self._create_summary(),
            responses=self._create_responses()
        )
        with open(self.json_output_file, "w") as f:
            json.dump(test_run.dict(), f, indent=2)
        print(f"✅ JSON results saved to {self.json_output_file}")

    def write_results(self):
        if self.output_format in [OutputFormat.TEXT, OutputFormat.BOTH]:
            self._write_text_results()

        if self.output_format in [OutputFormat.JSON, OutputFormat.BOTH]:
            self._write_json_results()

    # Original text formatting methods
    def _write_summary(self, file):
        file.write("SUMMARY\n")
        file.write(f"Date: {format_timestamp(self.metadata['first_timestamp'])}\n")
        file.write(f"Model: {self.metadata['model_name']}\n")
        file.write(f"Number of Questions: {self.metadata['question_count']}\n")
        file.write(f"Total Processing Time: {format_duration(self.metadata['total_duration'])}\n")
        file.write(f"Average Time per Question: {format_duration(self.metadata['total_duration']/self.metadata['question_count'])}\n")
        file.write(f"Total Tokens Used: {self.metadata['total_tokens']:,}\n")
        file.write(f"Average Tokens per Question: {self.metadata['total_tokens']/self.metadata['question_count']:,.0f}\n")
        file.write("\n" + "___" * 15 + "\n\n")
        file.write("INDIVIDUAL QUESTIONS\n")

    def _write_questions(self, file):
        for i, (question, result) in enumerate(self.results, 1):
            self._write_single_response(file, i, question, result)

    def _write_single_response(self, file, question_num: int, question: str, result: dict):
        file.write(f"\nQUESTION {question_num}: {question}\n")
        file.write(f"\nANSWER: {result['response']}\n")
        file.write("\nSOURCES:\n")
        for idx, source in enumerate(result['sources'], 1):
            file.write(f"  {idx}. {source}\n")
        file.write("\nDETAILS:\n")
        file.write(f"Processing Time: {format_duration(result['response_metadata']['total_duration'])}\n")
        file.write(f"Total Tokens: {result['usage_metadata']['total_tokens']}\n")
        file.write("\n" + "===" * 15 + "\n\n")
