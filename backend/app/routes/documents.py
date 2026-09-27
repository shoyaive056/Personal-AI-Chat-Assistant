"""
Document endpoints — upload a file into a conversation, delete one.

Uploading with no `conversation_id` starts a new conversation, the same
way sending a first chat message does (see services/chat_service.py) —
the two entry points share that behavior via ConversationService.
"""

import logging

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.document import DocumentUploadResponse
from app.services.conversation_service import ConversationService
from app.services.document_service import DocumentService, UnsupportedFileTypeError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    conversation_id: str | None = Form(default=None),
    db: Session = Depends(get_db),
) -> DocumentUploadResponse:
    """Extract text from an uploaded PDF/DOCX/TXT file and attach it to a
    conversation so the AI can reference it in later chat replies.
    """
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    file_bytes = await file.read()

    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. Maximum size is {settings.max_upload_size_mb} MB.",
        )

    conversations = ConversationService(db)
    documents = DocumentService(db)

    try:
        text = documents.extract_text(file.filename, file_bytes)
    except UnsupportedFileTypeError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except ValueError as exc:
        logger.warning("Document extraction failed for %s: %s", file.filename, exc)
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    conversation = None
    if conversation_id:
        conversation = conversations.get_conversation(conversation_id)
    if conversation is None:
        conversation = conversations.create_conversation(f"📄 {file.filename}")

    document = documents.save_document(conversation.id, file.filename, text)

    return DocumentUploadResponse(document=document, conversation_id=conversation.id)


@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: str, db: Session = Depends(get_db)) -> None:
    """Remove a document from its conversation."""
    documents = DocumentService(db)

    if not documents.delete_document(document_id):
        raise HTTPException(status_code=404, detail="Document not found.")