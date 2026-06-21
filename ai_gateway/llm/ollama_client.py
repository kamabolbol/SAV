import requests
import os
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

def query_ollama(model: str, prompt: str, context: dict = {}) -> str:
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }
    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "Aucune réponse.")
    except Exception as e:
        return f"Erreur Ollama : {str(e)}"
