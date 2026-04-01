import requests
from config import Config

class EmbeddingProcessor:
    """
    Handles generation of vector embeddings using Ollama.
    """
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = Config.OLLAMA_EMBED_MODEL

    def get_embedding(self, text: str):
        """
        Generates embedding for a given text via Ollama API.
        """
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": self.model,
            "prompt": text
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json().get('embedding')
        except Exception as e:
            print(f"Error generating embedding via Ollama: {e}")
            return None
