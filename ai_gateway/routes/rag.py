from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.retriever import query_collection
from llm.ollama_client import query_ollama
from security.filter import security_check
from logs.logger import log_request
import time
import os

router = APIRouter(prefix="/rag", tags=["rag"])

class RagRequest(BaseModel):
    question: str
    collection: str = "odoo_docs"
    user_id: int = 0

@router.post("/query")
async def rag_query(req: RagRequest):
    start = time.time()
    if not security_check(req.question):
        raise HTTPException(status_code=403, detail="Question rejected")
    docs = query_collection(req.collection, req.question, n_results=3)
    if not docs:
        return {"response": "Aucun document trouvé pour cette question."}
    context = "\n".join(docs)
    prompt = f"Basé sur les documents suivants :\n{context}\nRéponds à la question : {req.question}"
    model = os.getenv("AI_MODEL", "phi3:mini")
    response = query_ollama(model, prompt, context={})
    duration = int((time.time() - start) * 1000)
    log_request(req.user_id, "rag", req.question, response, model, duration)
    return {"response": response, "sources": docs}
