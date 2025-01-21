import pymupdf4llm
from langchain.text_splitter import MarkdownTextSplitter
from pprint import pprint

def main():
    documents = load_documents()
    pprint(documents)
    # chunks = split_documents(documents)


def load_documents():
    data = pymupdf4llm.to_markdown("./data/tattoo_inks_fg_2024-456_final_for_posting_10242024.pdf")

    #data2 = pymupdf4llm.to_markdown(".data/MERGED_cosmetic_guidances.pdf", page_chunks=True)
    splitter = MarkdownTextSplitter(chunk_size=90, chunk_overlap=8)

    splitter.create_documents([data])

    return data



# def split_documents(documents):






if __name__ == "__main__":
    main()
