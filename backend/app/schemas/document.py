"""Request/response validation models for document-related endpoints."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    """A stored document's metadata (never the full extracted text — that
    stays server-side and is only ever sent to the AI provider, not back
    to the client, to keep responses small).
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    char_count: int
    uploaded_at: datetime


class DocumentUploadResponse(BaseModel):
    """Body returned by POST /api/documents/upload."""

    document: DocumentOut
    conversation_id: str