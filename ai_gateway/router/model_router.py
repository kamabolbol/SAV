import os

MODEL = os.getenv("AI_MODEL", "phi3:mini")

TASK_MODEL_MAP = {
    "email": MODEL,
    "product": MODEL,
    "summary": MODEL,
    "analysis": MODEL,
    "chat": MODEL
}

def select_model(task: str) -> str:
    return TASK_MODEL_MAP.get(task, MODEL)
