from langchain_ollama import OllamaEmbeddings
from datetime import datetime

# Used to populate the vector db, and for the LLM to query the vector db
def process_embeddings():
    return OllamaEmbeddings(
        model="mxbai-embed-large"
    )

# Human readable formatting for the output time and date stamps
def format_timestamp(iso_timestamp):
    dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
    return dt.strftime("%d %b %Y at %H:%M")

def format_duration(nanoseconds):
    seconds = nanoseconds / 1_000_000_000
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    return f"{minutes}m {remaining_seconds:.2f}s" if minutes > 0 else f"{remaining_seconds:.2f}s"
