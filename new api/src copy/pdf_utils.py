from typing import List, Dict, Any
import pymupdf4llm

def process_pdf(file_path: str) -> List[Dict[str, Any]]:
    raw_data = pymupdf4llm.to_markdown(file_path, page_chunks=True)
    if not isinstance(raw_data, list):
        raise TypeError("Expected list from pymupdf4llm.to_markdown")
    pdf_data: List[Dict[str, Any]] = raw_data

    for page in pdf_data:
        if not isinstance(page, dict):
            continue

        # Get title, or set metadata title if field is empty
        metadata = page.get("metadata", {})
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

        # Update the metadata in the page dictionary
        page["metadata"] = metadata

    return pdf_data
