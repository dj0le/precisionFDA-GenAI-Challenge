from typing import List, Dict, Any
import pymupdf4llm

def process_pdf(file_path: str, file_id: str, file_hash: str) -> List[Dict[str, Any]]:
    raw_data = pymupdf4llm.to_markdown(file_path, page_chunks=True)
    if not isinstance(raw_data, list):
        raise TypeError("Expected list from pymupdf4llm.to_markdown")
    pdf_data: List[Dict[str, Any]] = raw_data

    for page in pdf_data:
        if not isinstance(page, dict):
            raise TypeError(f"Expected dictionary for page, got {type(page)}")

        metadata: Dict[str, Any] = page.get("metadata", {})
        if not isinstance(metadata, dict):
            metadata = {}

        source = metadata.get("title")
        if not source:
            file_path = metadata.get("file_path", "")
            filename = file_path.split('/')[-1].split('\\')[-1]
            filename = filename.rsplit('.', 1)[0]
            metadata["title"] = filename
            source = filename

        # Truncate filename
        if len(source) > 55:
            source = source[:52] + "..."

        page_num = metadata.get("page")
        page_id = f"{source}:{page_num}"
        metadata["id"] = page_id
        metadata["file_id"] = file_id
        metadata["file_hash"] = file_hash

        # Update the metadata in the page dictionary
        page["metadata"] = metadata

    return pdf_data
