from rag.chroma_client import get_collection
from rag.embedding import embed_text

def query_collection(collection_name: str, question: str, n_results: int = 3) -> list:
    collection = get_collection(collection_name)
    emb = embed_text(question)
    results = collection.query(query_embeddings=[emb], n_results=n_results)
    if results and results['documents']:
        return results['documents'][0]
    return []
