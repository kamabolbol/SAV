import logging
import os
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# ---------- Métriques Prometheus ----------
REQUESTS = Counter('ai_requests_total', 'Total number of AI requests')
LATENCY = Histogram('ai_request_latency_seconds', 'AI request latency', buckets=(0.01, 0.05, 0.1, 0.5, 1, 2.5, 5, 10))
ERRORS = Counter('ai_errors_total', 'Total number of AI errors', ['error_type'])

# ---------- Endpoint /metrics ----------
async def metrics_endpoint():
    return Response(content=generate_latest(), media_type="text/plain")

# ---------- OpenTelemetry (Tempo) ----------
def setup_telemetry(app):
    resource = Resource.create(attributes={"service.name": "ai-gateway"})
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="tempo:4317", insecure=True)
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Instrumenter FastAPI automatiquement
    FastAPIInstrumentor.instrument_app(app)

# ---------- Logs structurés JSON (Loki) ----------
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Supprimer les handlers existants (évite les doublons)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler()

    try:
        from pythonjsonlogger import jsonlogger
        formatter = jsonlogger.JsonFormatter(
            fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
            rename_fields={'levelname': 'severity', 'asctime': 'timestamp'}
        )
    except ImportError:
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Activer la propagation pour Uvicorn (comme dans Ray Serve)
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.propagate = True
    uvicorn_access_logger.setLevel(logging.INFO)

    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.propagate = True
