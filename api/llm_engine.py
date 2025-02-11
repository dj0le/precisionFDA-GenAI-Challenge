from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from config import settings
from utils.model_utils import process_embeddings
from utils.chroma_manager import ChromaManager
from typing import Dict, Any

class LLMQueryEngine:
    def __init__(self, chroma_path: str, embedding_function: Any, model: str):
        self.model = model
        self._db_manager = ChromaManager()
        self._db_manager.initialize(chroma_path, embedding_function)
        self._llm = ChatOllama(model=self.model, temperature=0)
        self._prompt_template = ChatPromptTemplate.from_template("""
            Answer the question based only on the following context: {context}
            ---
            Answer the question based on the above context: {question}
            """)

    def format_sources(self, documents):
        """Common source formatting logic"""
        return [
            f"{doc.metadata.get('original_filename', 'Unknown')} (page{doc.metadata.get('page_number', 0)})"
            for doc in documents
        ]

    def query(self, query_text: str) -> Dict[str, Any]:
        results = self._db_manager.search_documents(query_text)
        print(f"Found {len(results)} results for query: {query_text}")

        if not results:
            return {
                "response": "I don't have any documents in my database to answer your question.",
                "sources": [],
                "response_metadata": {},
                "usage_metadata": {}
            }

        documents = [doc for doc, _score in results]
        context_text = "\n\n---\n\n".join([doc.page_content for doc in documents])
        prompt = self._prompt_template.format(context=context_text, question=query_text)
        response = self._llm.invoke(prompt)

        return {
            "response": response.content,
            "sources": self.format_sources(documents),
            "response_metadata": response.response_metadata,
            "usage_metadata": getattr(response, 'usage_metadata', {})
        }

    def retrieve_relevant_documents(self, query_text: str):
        results = self._db_manager.search_documents(query_text)
        print(f"Retrieved {len(results)} documents for query: {query_text}")
        return [doc for doc, _score in results]
