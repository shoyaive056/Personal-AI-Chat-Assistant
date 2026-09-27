"""
Google Gemini provider.

Free-tier option: Google AI Studio issues API keys with a generous free
quota and no card required. Get one at https://aistudio.google.com/apikey.

Uses the `google-genai` SDK (the actively maintained one — the older
`google-generativeai` package has been fully deprecated by Google).

Gemini's API shape differs from OpenAI's (roles are "user"/"model" rather
than "user"/"assistant", and the system prompt is passed separately rather
than as a message), so this file does the translation. Nothing outside
this file needs to know that — the rest of the app only ever talks to the
`AIProvider` interface.
"""

from google import genai
from google.genai import errors as genai_errors
from google.genai import types as genai_types

from app.config import settings
from app.services.providers.base import AIProvider, ProviderMessage

# Gemini has no "assistant" role — it calls the model's own turns "model".
_GEMINI_ROLE_MAP = {"user": "user", "assistant": "model"}


class GeminiProvider(AIProvider):
    """Talks to the Google Gemini API."""

    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model
        self.model_name = settings.gemini_model
        self._temperature = settings.gemini_temperature
        self._max_tokens = settings.gemini_max_tokens

    async def generate_reply(self, messages: list[ProviderMessage]) -> str:
        system_instruction, history = self._split_system_prompt(messages)

        try:
            response = await self._client.aio.models.generate_content(
                model=self._model,
                contents=history,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=self._temperature,
                    max_output_tokens=self._max_tokens,
                ),
            )
        except genai_errors.APIError as exc:
            raise RuntimeError(f"Gemini API request failed: {exc}") from exc

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini API returned an empty response.")

        return text

    @staticmethod
    def _split_system_prompt(
        messages: list[ProviderMessage],
    ) -> tuple[str | None, list[dict]]:
        """Pull the system message out and translate the rest to Gemini's
        {role, parts} shape.
        """
        system_instruction: str | None = None
        history: list[dict] = []

        for message in messages:
            if message["role"] == "system":
                system_instruction = message["content"]
                continue
            history.append(
                {
                    "role": _GEMINI_ROLE_MAP.get(message["role"], "user"),
                     "parts": [{"text": message["content"]}],
                }
            )

        return system_instruction, history