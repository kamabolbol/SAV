from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str) -> list:
    return model.encode(text).tolist()

def embed_documents(docs: list) -> list:
    return [embed_text(doc) for doc in docs]
