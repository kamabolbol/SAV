from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from security.filter import security_check
from context.manager import build_context
from router.model_router import select_model
from llm.ollama_client import query_ollama
from logs.logger import log_request
import time

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    prompt: str
    user_id: int = 0
    context: dict = {}

@router.post("/")
async def chat(req: ChatRequest):
    start = time.time()
    if not security_check(req.prompt):
        raise HTTPException(status_code=403, detail="Prompt rejected by security policy")
    context = build_context(req.context, req.user_id)
    model = select_model("chat")
    response = query_ollama(model, req.prompt, context)
    duration = int((time.time() - start) * 1000)
    log_request(req.user_id, "chat", req.prompt, response, model, duration)
    return {"response": response}
