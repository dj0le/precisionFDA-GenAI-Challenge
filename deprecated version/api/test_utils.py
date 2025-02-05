import json
from typing import List
from langchain_core.documents import Document

def print_document_metadata(documents: List[Document], stage: str = ""):
    print(f"\n=== Document Metadata {stage} ===")
    for i, doc in enumerate(documents, 1):
        print(f"\nDocument {i} Metadata:")
        print(json.dumps(doc.metadata, indent=2, sort_keys=True))
        print(f"Content length: {len(doc.page_content)}")
