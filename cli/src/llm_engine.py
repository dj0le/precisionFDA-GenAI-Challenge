from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

class LLMQueryEngine:
    def __init__(self, chroma_path: str, embedding_function):
        self._db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)
        self._llm = ChatOllama(model="mistral-nemo", temperature=0)
        self._prompt_template = ChatPromptTemplate.from_template("""
            Answer the question based only on the following context: {context}
            ---
            Answer the question based on the above context: {question}
            """)

    def query(self, query_text: str) -> dict:
        results = self._db.similarity_search_with_score(query_text, k=3)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt = self._prompt_template.format(context=context_text, question=query_text)

        response = self._llm.invoke(prompt)
        sources = [doc.metadata.get("id", None) for doc, _score in results]

        return {
            "response": response.content,
            "sources": sources,
            "response_metadata": response.response_metadata,
            "usage_metadata": response.usage_metadata
        }
