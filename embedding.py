from langchain_ollama import OllamaEmbeddings


def getEmbedding():
    embedding = OllamaEmbeddings(model="mxbai-embed-large")
    return embedding
