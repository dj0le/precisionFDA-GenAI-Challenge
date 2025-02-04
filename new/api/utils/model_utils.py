import ollama
from langchain_ollama import OllamaEmbeddings

def get_available_models():
    """Return list of available models or set default to llama3.2"""
    try:
        model_list = ollama.list()
        return [model_info['model'].split(':')[0] for model_info in model_list['models']]
    except Exception:
        return ['llama3.2']

def refresh_available_models(self):
    """Refresh the list of available models"""
    self.AVAILABLE_MODELS = get_available_models()

def process_embeddings():
    """Initialize and return embedding model"""
    return OllamaEmbeddings(model="mxbai-embed-large")
