import argparse
from huggingface_hub.inference._generated.types import question_answering
from langchain_core.tools.retriever import create_retriever_tool
import pymupdf
import pymupdf4llm
import json
import shutil
import os
from langchain.chains import history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from pprint import pprint
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from typing import List

from langchain.schema import AIMessage, HumanMessage
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory

CHROMA_PATH = "chroma"

def main():
    # clear_database()
    folder_path = "./db_uploads"
    data = load_documents(folder_path)
    if data:
        create_ids(data)
        populate_vectordb(data)

def load_documents(folder_path: str) -> List[Document]:
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.pdf'):
            loader = PyMuPDFLoader(file_path)
        else:
            print(f"Unsupported file type: {filename}")
            continue
        documents.extend(loader.load())
        # print(f"✅ Loaded {len(documents)} documents from the folder.")
    return documents

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
    print(f"✅ Number of existing documents in DB: {len(db_ids)}")

    # Prepare new documents for db
    new_documents = []
    new_ids = []
    new_metadatas = []

    for doc in data:
        page_id = doc.metadata["id"]
        if page_id not in db_ids:
            cleaned_metadata = {
                k: v for k, v in doc.metadata.items()
                if v is not None and isinstance(v, (str, int, float, bool))
            }

            new_documents.append(doc.page_content)
            new_ids.append(page_id)
            new_metadatas.append(cleaned_metadata)

    if new_documents:
        print(f"✅ Adding new documents: {len(new_documents)}")
        db.add_texts(
            texts=new_documents,
            ids=new_ids,
            metadatas=new_metadatas
        )

        print("✅ Documents added successfully")
    else:
        print("✅ No new documents to add")

    return db


def create_ids(data: List[Document]):
    for page in data:
        # Get title, or set metadata title if field is empty
        source = page.metadata.get("title")
        if not source:
            file_path = page.metadata.get("source", "")
            filename = file_path.split('/')[-1].split('\\')[-1]
            filename = filename.rsplit('.', 1)[0]
            page.metadata["title"] = filename
            source = filename

        page_num = page.metadata.get("page")
        page_id = f"{source}:{page_num}"
        page.metadata["id"] = page_id

    return data

def process_embeddings():
    return OllamaEmbeddings(
        model="mxbai-embed-large"
    )

# def build_chain(query_text: str, chat_history=[]):
#     db = Chroma(
#         persist_directory=CHROMA_PATH, embedding_function=process_embeddings()
#     )

#     retriever = db.as_retriever(search_kwargs={"k": 2})

#     llm = ChatOllama(
#         model="llama3.2",
#         temperature=0
#     )

#     # Create memory
#     memory = ConversationBufferMemory(
#         memory_key="chat_history",
#         return_messages=True,
#         output_key="answer"
#     )

#     # Create the conversational chain
#     chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=retriever,
#         memory=memory,
#         return_source_documents=True,
#         # verbose=True
#     )

#     # Get response
#     result = chain({"question": query_text})

#     # Extract answer and sources
#     answer = result['answer']
#     sources = [doc.metadata.get("id", None) for doc in result.get('source_documents', [])]

#     formatted_response = f"\n-----\n Question: {query_text}\n-------\n Answer: {answer}\n-----\n Sources:"
#     print(formatted_response)
#     print(json.dumps(sources, indent=4))

#     return result

def build_chain(query_text: str):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=process_embeddings()
    )

    answers = db.similarity_search_with_score(query_text, k=4)

    template  = """Answer the question based only on the following context: {context}
    Question: {question}
    Answer: """

    prompt = ChatPromptTemplate.from_template(template)

    def doc2str(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    output_parser = StrOutputParser()

    retriever = db.as_retriever(search_kwargs={"k": 2})

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "Use only the context provided to answer user questions"),
        ("system", "Context: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


    rag_chain = (
        {"context": retriever | doc2str, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    question = query_text
    answer = rag_chain.invoke(question)
    sources = [doc.metadata.get("id", None) for doc, _score in answers]
    formatted_response = f"\n-----\n Question: {question}\n-------\n Answer: {answer}\n-----\n Sources:"
    print(formatted_response)
    print(json.dumps(sources, indent=4))


    rag_chain.invoke({"input": "Which standard is referenced?", "chat_history":chat_history})

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
