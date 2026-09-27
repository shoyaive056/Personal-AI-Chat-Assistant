"""
Conversation endpoints — list, fetch, and delete saved conversations.

Creating a conversation is not a separate endpoint: POST /api/chat creates
one automatically the first time a message is sent without a
`conversation_id` (see services/chat_service.py).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.conversation import ConversationDetail, ConversationSummary
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("", response_model=list[ConversationSummary])
def list_conversations(db: Session = Depends(get_db)) -> list[ConversationSummary]:
    """All conversations, most recently active first — for the sidebar."""
    service = ConversationService(db)
    return service.list_conversations()


@router.get("/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: str, db: Session = Depends(get_db)
) -> ConversationDetail:
    """A single conversation with its full message history."""
    service = ConversationService(db)
    conversation = service.get_conversation(conversation_id)

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    return conversation


@router.delete("/{conversation_id}", status_code=204)
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)) -> None:
    """Delete a conversation and all of its messages."""
    service = ConversationService(db)

    if not service.delete_conversation(conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found.")