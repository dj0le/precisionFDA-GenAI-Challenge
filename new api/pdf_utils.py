import pymupdf4llm
from typing import List
from langchain_core.documents import Document

def process_pdf(file_path: str) -> List[Document]:
    pdf_data = pymupdf4llm.to_markdown(file_path, page_chunks=True)

    documents = []

    for page in pdf_data:
        # remove None and non-primitive types
        clean_metadata = {
            k: v for k, v in page["metadata"].items()
            if v is not None and isinstance(v, (str, int, float, bool))
        }

        # Get title, or set metadata title if field is empty
        source = clean_metadata.get("title")
        if not source:
            file_path = clean_metadata.get("file_path", "")
            filename = file_path.split('/')[-1].split('\\')[-1]
            filename = filename.rsplit('.', 1)[0]
            clean_metadata["title"] = filename
            source = filename

        # Truncate filename
        if len(source) > 55:
            source = source[:52] + "..."

        page_num = clean_metadata.get("page")
        page_id = f"{source}:{page_num}"
        clean_metadata["id"] = page_id

        # Return Langchain Document
        doc = Document(
            page_content=page["text"],
            metadata=clean_metadata
        )
        documents.append(doc)

    return documents


# Test the function
# pdf_data = process_pdf("./atest.pdf")
# if pdf_data:
#     print(f"\nDocument loaded successfully! Number of pages: {len(pdf_data)}")

#     print("\nFirst page metadata:")
#     for key, value in pdf_data[4].metadata.items():
#         print(f"  {key}: {value}")

#     print("\nPage contents:")
#     print(pdf_data[4].page_content)
