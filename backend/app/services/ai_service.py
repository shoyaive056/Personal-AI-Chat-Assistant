"""
AI provider factory.

This module is the only place in the codebase that knows how to construct
a concrete `AIProvider`. To add a new provider (Anthropic, a local model,
etc.), implement `AIProvider` in `services/providers/`, register it in
`_PROVIDERS` below, and set `AI_PROVIDER` in the environment — nothing
else in the application needs to change.
"""

from functools import lru_cache

from app.config import settings
from app.services.providers.base import AIProvider
from app.services.providers.gemini_provider import GeminiProvider
from app.services.providers.groq_provider import GroqProvider
from app.services.providers.openai_provider import OpenAIProvider

_PROVIDERS: dict[str, type[AIProvider]] = {
    "openai": OpenAIProvider,
    "groq": GroqProvider,
    "gemini": GeminiProvider,
}


@lru_cache
def get_ai_provider() -> AIProvider:
    """Return the configured AI provider (cached as a singleton)."""
    provider_cls = _PROVIDERS.get(settings.ai_provider)

    if provider_cls is None:
        available = ", ".join(_PROVIDERS)
        raise RuntimeError(
            f"Unknown AI_PROVIDER '{settings.ai_provider}'. "
            f"Available providers: {available}"
        )

    return provider_cls()