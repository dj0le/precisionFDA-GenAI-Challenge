from typing import List, Dict, Any
from datetime import datetime
from utils.formatting import format_timestamp, format_duration
from utils.pydantic_models import BatchSummary, QuestionResponse, BatchQueryResponse
import json

class BatchResultsProcessor:
    def __init__(self, model_name: str):
        self.results: List[Dict[str, Any]] = []
        self.metadata = {
            "total_duration": 0,
            "total_tokens": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "model_name": model_name,
            "question_count": 0
        }

    def add_result(self, question: str, result: Dict[str, Any]) -> None:
        self.results.append({
            "question": question,
            "result": result
        })
        self._update_metadata(result)
        self.metadata["question_count"] += 1

    def _update_metadata(self, result: Dict[str, Any]) -> None:
        self.metadata["total_duration"] += result['response_metadata']['total_duration']
        self.metadata["total_tokens"] += result['usage_metadata']['total_tokens']

    def get_formatted_results(self) -> BatchQueryResponse:
        summary = BatchSummary(
            timestamp=self.metadata["timestamp"],
            model=self.metadata["model_name"],
            question_count=self.metadata["question_count"],
            total_processing_time_ns=self.metadata["total_duration"],
            avg_processing_time_ns=self.metadata["total_duration"] / max(1, self.metadata["question_count"]),
            total_tokens=self.metadata["total_tokens"],
            avg_tokens_per_question=self.metadata["total_tokens"] / max(1, self.metadata["question_count"])
        )

        responses = [
            QuestionResponse(
                question_number=i + 1,
                question=item["question"],
                answer=item["result"]["response"],
                sources=item["result"]["sources"],
                processing_time_ns=item["result"]["response_metadata"]["total_duration"],
                total_tokens=item["result"]["usage_metadata"]["total_tokens"],
                metadata={
                    "response_metadata": item["result"]["response_metadata"],
                    "usage_metadata": item["result"]["usage_metadata"]
                }
            )
            for i, item in enumerate(self.results)
        ]

        return BatchQueryResponse(summary=summary, responses=responses)

    def to_text(self) -> str:
        output = []
        # Summary section
        output.append("SUMMARY")
        output.append(f"Date: {format_timestamp(self.metadata['timestamp'])}")
        output.append(f"Model: {self.metadata['model_name']}")
        output.append(f"Number of Questions: {self.metadata['question_count']}")
        output.append(f"Total Processing Time: {format_duration(self.metadata['total_duration'])}")
        output.append(f"Average Time per Question: {format_duration(self.metadata['total_duration']/max(1, self.metadata['question_count']))}")
        output.append(f"Total Tokens Used: {self.metadata['total_tokens']:,}")
        output.append(f"Average Tokens per Question: {self.metadata['total_tokens']/max(1, self.metadata['question_count']):,.0f}")

        # Questions section
        output.append("\n" + "="*50 + "\n")
        output.append("INDIVIDUAL QUESTIONS")

        for i, item in enumerate(self.results, 1):
            output.append(f"\nQUESTION {i}: {item['question']}")
            output.append(f"\nANSWER: {item['result']['response']}")
            output.append("\nSOURCES:")
            for idx, source in enumerate(item['result']['sources'], 1):
                output.append(f"  {idx}. {source}")
            output.append("\nDETAILS:")
            output.append(f"Processing Time: {format_duration(item['result']['response_metadata']['total_duration'])}")
            output.append(f"Total Tokens: {item['result']['usage_metadata']['total_tokens']}")
            output.append("\n" + "-"*50)

        return "\n".join(output)
