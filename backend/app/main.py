"""
FastAPI application entrypoint.

Keeps only app wiring here: middleware, router registration and startup
checks. Everything else (config, business logic, AI integration) lives in
its own module.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routes import chat, conversations, documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Shoyaive AI API",
    description="Backend API for Shoyaive AI, a personal AI assistant.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(conversations.router)
app.include_router(documents.router)


@app.on_event("startup")
async def validate_configuration() -> None:
    """Fail fast and loudly if required environment variables are missing."""
    try:
        settings.validate()
    except RuntimeError as exc:
        logger.error(str(exc))
        raise


@app.on_event("startup")
async def create_database_tables() -> None:
    """Create tables that don't exist yet. Safe to run on every startup."""
    init_db()


@app.get("/api/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Simple liveness check used by the frontend and for manual testing."""
    return {"status": "ok", "environment": settings.environment}