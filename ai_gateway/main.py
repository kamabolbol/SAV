from fastapi import FastAPI
from routes import chat, generate, rag

app = FastAPI(title="AI Gateway for Odoo", version="1.0")

app.include_router(chat.router)
app.include_router(generate.router)
app.include_router(rag.router)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
