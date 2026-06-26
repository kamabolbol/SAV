from fastapi import FastAPI, Request
import time
import logging
from routes import chat, generate, rag
from observability import (
    setup_telemetry,
    setup_logging,
    metrics_endpoint,
    REQUESTS,
    LATENCY,
    ERRORS
)

app = FastAPI(title="AI Gateway for Odoo", version="1.0")

# ---------- Initialisation de l'observabilité ----------
setup_telemetry(app)
setup_logging()

# ---------- Route /metrics ----------
app.add_api_route("/metrics", metrics_endpoint, methods=["GET"])

# ---------- Middleware pour les métriques ----------
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    REQUESTS.inc()

    try:
        response = await call_next(request)
        latency = time.time() - start_time
        LATENCY.observe(latency)
        return response
    except Exception as e:
        ERRORS.labels(error_type=type(e).__name__).inc()
        raise

# ---------- Routes existantes ----------
app.include_router(chat.router)
app.include_router(generate.router)
app.include_router(rag.router)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)