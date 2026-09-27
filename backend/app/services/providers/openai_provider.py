"""OpenAI chat-completions provider."""

from openai import AsyncOpenAI, OpenAIError

from app.config import settings
from app.services.providers.base import AIProvider, ProviderMessage


class OpenAIProvider(AIProvider):
    """Talks to the OpenAI Chat Completions API."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model
        self.model_name = settings.openai_model
        self._temperature = settings.openai_temperature
        self._max_tokens = settings.openai_max_tokens

    async def generate_reply(self, messages: list[ProviderMessage]) -> str:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )
        except OpenAIError as exc:
            # Re-raised as a plain exception; the route layer decides how
            # to translate this into an HTTP response.
            raise RuntimeError(f"OpenAI API request failed: {exc}") from exc

        choice = response.choices[0] if response.choices else None
        content = choice.message.content if choice and choice.message else None

        if not content:
            raise RuntimeError("OpenAI API returned an empty response.")

        return content