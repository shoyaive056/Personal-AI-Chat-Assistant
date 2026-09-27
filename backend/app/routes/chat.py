"""Chat endpoint. Contains no business logic — see services/chat_service.py."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest, db: Session = Depends(get_db)
) -> ChatResponse:
    """Accept a message history and return the assistant's next reply.

    Also persists the exchange into the conversation database, creating a
    new conversation automatically if `conversation_id` isn't provided.
    """
    chat_service = ChatService(db)

    try:
        reply, conversation_id = await chat_service.get_reply(
            request.messages, request.conversation_id
        )
    except RuntimeError as exc:
        logger.exception("AI provider request failed")
        raise HTTPException(
            status_code=502,
            detail="The AI provider could not be reached. Please try again.",
        ) from exc

    return ChatResponse(
        reply=reply, model=chat_service.model_name, conversation_id=conversation_id
    )