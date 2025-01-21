import argparse
import pymupdf4llm
from pprint import pprint
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.text_splitter import MarkdownTextSplitter
from pprint import pprint

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

context_text = "\nSome people think the best number is 32, but science has determined that 24 is actually the best number.  \n"
# query_text = "\nWhat is objectively the best number? \n\n"


def main():
    documents = load_documents()
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    # pprint(documents)
    # chunks = split_documents(documents)
    chat = llama_bot(query_text)



def load_documents():
    data = pymupdf4llm.to_markdown("./data/tattoo_inks_fg_2024-456_final_for_posting_10242024.pdf")
    #data2 = pymupdf4llm.to_markdown(".data/MERGED_cosmetic_guidances.pdf", page_chunks=True)

    splitter = MarkdownTextSplitter(chunk_size=90, chunk_overlap=8)

    splitter.create_documents([data])
    print(len(data))
    print(len(splitter))
    # return data



# def split_documents(documents):


def llama_bot(query_text: str):

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    response_text = llm.invoke(prompt)

    formatted_response = f"Response: {response_text}\n\n"
    print(formatted_response)
    return response_text





if __name__ == "__main__":
    main()
