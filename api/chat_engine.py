from config import settings
from llm_engine import LLMQueryEngine
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from utils.model_utils import process_embeddings
from utils.formatting import format_duration

# define new prompt template for chat and historical context
format_question_prompt = """
You are a professional AI researcher tasked with providing accurate and detailed answers based on the given context.
Rules:
1. Only use information present in the provided context
2. If you can't find the answer in the context, clearly state that
3. Maintain continuity with previous conversation while focusing on the current question
4. Cite specific parts of the context when possible

Context: {context}
"""

class ChatEngine:
    """
        Handles chat interactions with context awareness and history management
    """
    def __init__(self, model: str):
        self.llm_engine = LLMQueryEngine(
            chroma_path=settings.CHROMA_PATH,
            embedding_function=process_embeddings(),
            model=model
        )
        self.llm = ChatOllama(model=model, temperature=0)

        self.context_prompt = ChatPromptTemplate.from_messages([
            ("system", format_question_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

    def get_response(self, query: str, chat_history: list):
        documents = self.llm_engine.retrieve_relevant_documents(query)

        if not documents:
            return self.llm_engine.query(query)

        context = "\n\n---\n\n".join([doc.page_content for doc in documents])
        prompt = self.context_prompt.format(
            context=context,
            chat_history=chat_history,
            input=query
        )

        response = self.llm.invoke(prompt)

        return {
            "response": response.content,
            "sources": self.llm_engine.format_sources(documents),
            "response_metadata": response.response_metadata,
            "usage_metadata": getattr(response, 'usage_metadata', {})
        }
