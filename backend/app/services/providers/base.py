"""
Provider interface.

Every AI provider (OpenAI today; Anthropic, local models, etc. later) must
implement this interface. The rest of the application talks to providers
only through this contract, so swapping providers never requires changing
routes or higher-level services.
"""

from abc import ABC, abstractmethod
from typing import TypedDict


class ProviderMessage(TypedDict):
    role: str
    content: str


class AIProvider(ABC):
    """Common interface for chat-completion providers."""

    @abstractmethod
    async def generate_reply(self, messages: list[ProviderMessage]) -> str:
        """Given the full message history (including the system message),
        return the assistant's reply text.
        """
        raise NotImplementedError
