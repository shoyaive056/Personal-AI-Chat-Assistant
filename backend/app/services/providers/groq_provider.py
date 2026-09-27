"""
Groq chat-completions provider.

Groq exposes an OpenAI-compatible API, so this reuses the same `openai`
SDK already installed for OpenAIProvider — the only difference is
`base_url` and the API key/model that get passed in. This is the
free-tier option: https://console.groq.com/keys (no card required).
"""

from openai import AsyncOpenAI, OpenAIError

from app.config import settings
from app.services.providers.base import AIProvider, ProviderMessage

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


class GroqProvider(AIProvider):
    """Talks to Groq's OpenAI-compatible Chat Completions API."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.groq_api_key,
            base_url=GROQ_BASE_URL,
        )
        self._model = settings.groq_model
        self.model_name = settings.groq_model
        self._temperature = settings.groq_temperature
        self._max_tokens = settings.groq_max_tokens

    async def generate_reply(self, messages: list[ProviderMessage]) -> str:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )
        except OpenAIError as exc:
            raise RuntimeError(f"Groq API request failed: {exc}") from exc

        choice = response.choices[0] if response.choices else None
        content = choice.message.content if choice and choice.message else None

        if not content:
            raise RuntimeError("Groq API returned an empty response.")

        return content