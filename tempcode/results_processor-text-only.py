from src.config_utils import format_timestamp, format_duration

class ResultsProcessor:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.results = []
        self.metadata = {
            "total_duration": 0,
            "total_tokens": 0,
            "first_timestamp": None,
            "model_name": None,
            "question_count": 0
        }

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

    def write_results(self):
        with open(self.output_file, "w") as f:
            self._write_summary(f)
            self._write_questions(f)
        print(f"✅ All questions processed. Results saved to {self.output_file}")

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
