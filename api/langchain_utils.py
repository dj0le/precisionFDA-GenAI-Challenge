import os
import streamlit as st
from chroma_utils import vectorstore
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from typing import List


retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
output_parser = StrOutputParser()


# setup prompt to include message history as context
add_context_prompt = """
Given the chat history and the latest user question, formulate a search-optimized question that:
1. Captures the full context of the conversation
2. Includes relevant details from the chat history
3. Can be used to find appropriate information in a document database
4. Maintains the original intent of the user's question

Your task is to reformulate the question to be more detailed and search-friendly, not to answer it.
If the question is already well-formed and specific, you can return it as is.
"""

updated_prompt = ChatPromptTemplate.from_messages([
    ("system", add_context_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# update prompt and define output style
format_question_prompt = """
You are a professional AI researcher tasked with providing accurate and detailed answers based on the given context.
Rules:
1. Only use information present in the provided context
2. If you can't find the answer in the context, clearly state that
3. Maintain continuity with previous conversation while focusing on the current question
4. Cite specific parts of the context when possible

Context: {context}
"""

question_prompt = ChatPromptTemplate.from_messages([
    ("system", format_question_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def build_chain(model=None):
    model_name = st.session_state.get("model")
    llm = ChatOllama(model=model, temperature=0)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, updated_prompt)
    response_chain = create_stuff_documents_chain(llm, question_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, response_chain)
    return rag_chain
