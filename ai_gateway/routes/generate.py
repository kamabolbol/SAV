from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prompts.manager import load_template
from security.filter import security_check
from router.model_router import select_model
from llm.ollama_client import query_ollama
from logs.logger import log_request
import time

router = APIRouter(prefix="/generate", tags=["generate"])

class GenerateRequest(BaseModel):
    task: str
    data: dict = {}
    user_id: int = 0

@router.post("/")
async def generate(req: GenerateRequest):
    start = time.time()
    prompt_template = load_template(req.task)
    prompt = prompt_template.format(**req.data)
    if not security_check(prompt):
        raise HTTPException(status_code=403, detail="Prompt rejected")
    model = select_model(req.task)
    response = query_ollama(model, prompt, context={})
    duration = int((time.time() - start) * 1000)
    log_request(req.user_id, req.task, prompt, response, model, duration)
    return {"response": response}

@router.post("/product")
async def generate_product(data: dict, user_id: int = 0):
    req = GenerateRequest(task="product", data=data, user_id=user_id)
    return await generate(req)

@router.post("/email")
async def generate_email(data: dict, user_id: int = 0):
    req = GenerateRequest(task="email", data=data, user_id=user_id)
    return await generate(req)
