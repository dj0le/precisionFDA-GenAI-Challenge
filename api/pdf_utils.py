import os, pymupdf4llm
from langchain_core.documents import Document
from typing import List

def process_pdf(file_path: str) -> List[Document]:
    """
    Process PDF file and return list of Documents with proper metadata and IDs
    """
    pdf_data = pymupdf4llm.to_markdown(file_path, page_chunks=True)
    documents = []
    first_page_metadata = None

    for page in pdf_data:
        # Get or create title
        title = page["metadata"].get("title")
        if not title:
            title = os.path.basename(file_path).rsplit('.', 1)[0]

        # Create page ID
        page_num = page["metadata"].get("page")
        page_id = f"{title}:{page_num}"

        # Create metadata dictionary
        metadata = {
            "source": file_path,
            "page": page_num,
            "title": title,
            "id": page_id
        }

        # Create Document object
        doc = Document(
            page_content=page["text"],
            metadata=metadata
        )
        documents.append(doc)

    return documents
