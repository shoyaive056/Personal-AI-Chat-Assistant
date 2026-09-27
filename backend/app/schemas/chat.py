"""Request/response validation models for chat-related endpoints."""

from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["user", "assistant"]


class ChatMessage(BaseModel):
    """A single turn in the conversation, as sent by the client."""

    role: Role
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    """Body of POST /api/chat.

    The client sends the full message history so the AI call itself stays
    simple and stateless from the provider's point of view.
    `conversation_id` is optional: omit it to start a new conversation
    (the backend creates one and returns its id), or pass an existing id
    to keep persisting messages into that same conversation.
    """

    messages: list[ChatMessage] = Field(..., min_length=1)
    conversation_id: str | None = Field(
        default=None,
        description="Existing conversation to save into. Omit to start a new one.",
    )


class ChatResponse(BaseModel):
    """Body returned by POST /api/chat."""

    reply: str
    model: str
    conversation_id: str