import pymupdf4llm
from langchain.text_splitter import MarkdownTextSplitter

def main():
    load_documents()


def load_documents():
    md_data = pymupdf4llm.to_markdown("./data/tattoo_inks_fg_2024-456_final_for_posting_10242024.pdf", page_chunks=True)

    splitter = MarkdownTextSplitter(chunk_size=90, chunk_overlap=8)
    split_documents = splitter.create_documents([md_data])
    print(split_documents)




if __name__ == "__main__":
    main()
