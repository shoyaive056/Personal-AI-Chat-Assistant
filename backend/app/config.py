"""
Application configuration.

All environment-dependent values live here and nowhere else. Services and
routes should import `settings` from this module instead of calling
`os.getenv` directly — that keeps configuration centralized and makes it
easy to see every setting the app depends on in one place.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Typed access to environment configuration."""

    def __init__(self) -> None:
        # --- AI provider -----------------------------------------------
        self.ai_provider: str = os.getenv("AI_PROVIDER", "openai")

        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.openai_temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.openai_max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))

        # Groq (free-tier option) — OpenAI-compatible API, so it reuses the
        # same `openai` SDK under the hood, just pointed at a different
        # base URL. See services/providers/groq_provider.py.
        self.groq_api_key: str = os.getenv("GROQ_API_KEY", "")
        self.groq_model: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
        self.groq_temperature: float = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
        self.groq_max_tokens: int = int(os.getenv("GROQ_MAX_TOKENS", "1000"))

        # Gemini (free-tier option) — Google AI Studio API, no card
        # required. See services/providers/gemini_provider.py.
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.gemini_temperature: float = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        self.gemini_max_tokens: int = int(os.getenv("GEMINI_MAX_TOKENS", "1000"))

        # --- Server ------------------------------------------------------
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.environment: str = os.getenv("ENVIRONMENT", "development")

        # --- CORS ---------------------------------------------------------
        raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
        self.cors_origins: list[str] = [
            origin.strip() for origin in raw_origins.split(",") if origin.strip()
        ]
        # --- Database -------------------------------------------------------
        # SQLite by default — a single file, no server to run. Swapping to
        # PostgreSQL later (per the roadmap) is just changing this URL and
        # adding a driver (psycopg2/asyncpg) to requirements.txt; nothing
        # else in the app needs to change.
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./shoyaive.db")
            # --- Document upload --------------------------------------------------
        # Documents are injected into the AI's context as plain text (no
        # RAG/embeddings yet — that's a separate future feature for large
        # documents and a personal knowledge base). These limits keep a
        # single upload from blowing up the prompt size or the request body.
        self.max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
        self.max_document_chars: int = int(
            os.getenv("MAX_DOCUMENT_CHARS", "12000")
        )
    
    def validate(self) -> None:
        """Raise a clear error early if required configuration is missing."""
        if self.ai_provider == "openai" and not self.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to backend/.env "
                "(see .env.example)."
            )
        if self.ai_provider == "groq" and not self.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to backend/.env "
                "(see .env.example). Get a free key at "
                "https://console.groq.com/keys"
            )
        if self.ai_provider == "gemini" and not self.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to backend/.env "
                "(see .env.example). Get a free key at "
                "https://aistudio.google.com/apikey"
            )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (loaded once per process)."""
    return Settings()


settings = get_settings()