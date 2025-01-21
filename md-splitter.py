import pymupdf4llm
from langchain.text_splitter import MarkdownTextSplitter

data = pymupdf4llm.to_markdown("MERGED_cosmetic_guidances.pdf")

splitter = MarkdownTextSplitter(chunk_size=90, chunk_overlap=8)

splitter.create_documents([data])
print(len(data))
print(len(splitter))
