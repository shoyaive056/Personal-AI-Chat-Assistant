"""Request/response validation models for conversation-related endpoints."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageOut(BaseModel):
    """A single stored message, as returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    role: str
    content: str
    created_at: datetime


class ConversationSummary(BaseModel):
    """A conversation without its messages — used for the sidebar list."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationDetail(ConversationSummary):
    """A conversation including its full message history."""

    messages: list[MessageOut]