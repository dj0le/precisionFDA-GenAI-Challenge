import argparse
import pymupdf4llm
import json
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import MarkdownTextSplitter
from pprint import pprint

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context: {context}

---

Answer the question based on the above context: {question}
"""


def main():
    data = load_documents()
    if data:
        print("First page metadata:")
        create_ids(data)
        print(json.dumps(data[0]["metadata"], indent=4))
        populate_vectordb(data)

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    chat = query_llm(query_text)


def load_documents():
    try:
        file_path = input("Please enter the path to your PDF document: ")

        if not file_path.endswith('.pdf'):
            raise ValueError("File must be a PDF document")

        # Convert PDF to list of DICTs with metadata
        pdf_data = process_pdf(file_path)

        print(f"Document loaded successfully! Number of pages: {len(pdf_data)}")
        return pdf_data

    except FileNotFoundError:
        print("Error: File not found. Please check the file path and try again.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def process_pdf(file_path):
    data = pymupdf4llm.to_markdown(file_path, page_chunks=True)
    return data

def populate_vectordb(data: dict):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=process_embeddings()
    )

    # Add or Update the documents
    db_items = db.get(include=[])
    db_ids = set(db_items["ids"])
    print(f"Number of existing documents in DB: {len(db_ids)}")

    # Prepare new documents for addition
    new_documents = []
    new_ids = []
    new_metadatas = []

    for page in data:
        page_id = page["metadata"]["id"]
        if page_id not in db_ids:
            cleaned_metadata = {
                k: v for k, v in page["metadata"].items()
                if v is not None and isinstance(v, (str, int, float, bool))
            }

            new_documents.append(page["text"])
            new_ids.append(page_id)
            new_metadatas.append(cleaned_metadata)

    if new_documents:
        print(f"👉 Adding new documents: {len(new_documents)}")
        db.add_texts(
            texts=new_documents,
            ids=new_ids,
            metadatas=new_metadatas
        )

        print("✅ Documents added successfully")
    else:
        print("✅ No new documents to add")

    return db


def create_ids(data: dict):
    for page in data:
        # Get title, or set metadata title if field is empty
        source = page["metadata"].get("title")
        if not source:
            file_path = page["metadata"].get("file_path", "")
            filename = file_path.split('/')[-1].split('\\')[-1]
            filename = filename.rsplit('.', 1)[0]
            page["metadata"]["title"] = filename
            source = filename

        page_num = page["metadata"].get("page")
        page_id = f"{source}:{page_num}"
        page["metadata"]["id"] = page_id

    return data

def process_embeddings():
    return OllamaEmbeddings(
        model="mxbai-embed-large"
    )

def query_llm(query_text: str):
    embedding = process_embeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)

    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    response_text = llm.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
