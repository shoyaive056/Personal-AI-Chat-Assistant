"""
Conversation persistence.

All database access for conversations and messages lives here — routes
and other services never touch the ORM models directly. This keeps the
data layer swappable (SQLite today, PostgreSQL later) behind one file.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.conversation import Conversation, Message

_TITLE_MAX_LENGTH = 50


class ConversationService:
    """CRUD operations for conversations and their messages."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def list_conversations(self) -> list[Conversation]:
        """Most recently updated conversation first."""
        return (
            self._db.query(Conversation)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return (
            self._db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

    def create_conversation(self, first_message: str | None = None) -> Conversation:
        conversation = Conversation(title=self._derive_title(first_message))
        self._db.add(conversation)
        self._db.commit()
        self._db.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: str) -> bool:
        conversation = self.get_conversation(conversation_id)
        if conversation is None:
            return False
        self._db.delete(conversation)
        self._db.commit()
        return True

    def add_message(self, conversation_id: str, role: str, content: str) -> Message:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        self._db.add(message)

        conversation = self.get_conversation(conversation_id)
        if conversation is not None:
            # `message.created_at` isn't populated until the insert is
            # flushed, so compute the timestamp explicitly here instead.
            conversation.updated_at = datetime.now(timezone.utc)

        self._db.commit()
        self._db.refresh(message)
        return message

    @staticmethod
    def _derive_title(first_message: str | None) -> str:
        """A short, human-readable title from the conversation's first message."""
        if not first_message:
            return "New conversation"

        title = " ".join(first_message.split())
        if len(title) > _TITLE_MAX_LENGTH:
            title = title[:_TITLE_MAX_LENGTH].rstrip() + "…"

        return title or "New conversation"