import chromadb
from chromadb.config import Settings
import os
CHROMA_PATH = os.getenv("CHROMA_PATH", "/app/chroma_db")
client = chromadb.PersistentClient(path=CHROMA_PATH, settings=Settings(anonymized_telemetry=False))

def get_collection(name: str):
    try:
        return client.get_collection(name)
    except:
        return client.create_collection(name)
