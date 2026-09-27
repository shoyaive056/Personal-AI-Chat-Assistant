"""
Chat business logic.

Keeps the "what does a chat request actually do" logic out of the route
handler, so the route stays a thin HTTP layer and this logic stays
reusable (e.g. by a future WebSocket endpoint, a CLI, or a background
job) without duplicating it.
"""

from sqlalchemy.orm import Session

from app.prompts.system_prompt import CHAT_SYSTEM_PROMPT
from app.schemas.chat import ChatMessage
from app.services.ai_service import get_ai_provider
from app.services.conversation_service import ConversationService
from app.services.document_service import DocumentService
from app.services.providers.base import ProviderMessage


class ChatService:
    """Coordinates turning a chat request into an AI reply, persisting
    both sides of the exchange along the way.
    """

    def __init__(self, db: Session) -> None:
        self._provider = get_ai_provider()
        self._conversations = ConversationService(db)
        self._documents = DocumentService(db)

    @property
    def model_name(self) -> str:
        """Name of the model actually answering (depends on AI_PROVIDER)."""
        return self._provider.model_name

    async def get_reply(
        self, messages: list[ChatMessage], conversation_id: str | None
    ) -> tuple[str, str]:
        """Build the full prompt (system + documents + history), get the
        AI's reply, save the new user message and the reply, and return
        (reply, conversation_id).

        A new conversation is created automatically when `conversation_id`
        is None or doesn't match an existing conversation. Any documents
        already uploaded into that conversation are automatically included
        as context — the client doesn't need to resend them.
        """
        conversation = None
        if conversation_id:
            conversation = self._conversations.get_conversation(conversation_id)

        if conversation is None:
            first_message = messages[0].content if messages else None
            conversation = self._conversations.create_conversation(first_message)

        provider_messages: list[ProviderMessage] = [
            {"role": "system", "content": CHAT_SYSTEM_PROMPT},
        ]

        documents = self._documents.get_documents_for_conversation(conversation.id)
        document_context = self._documents.build_context_text(documents)
        if document_context:
            provider_messages.append({"role": "system", "content": document_context})

        provider_messages.extend(
            {"role": m.role, "content": m.content} for m in messages
        )
        reply = await self._provider.generate_reply(provider_messages)

        # The client sends the full history each time, so only the newest
        # user message is actually new to us — save that plus the reply.
        latest_user_message = messages[-1]
        self._conversations.add_message(
            conversation.id, latest_user_message.role, latest_user_message.content
        )
        self._conversations.add_message(conversation.id, "assistant", reply)

        return reply, conversation.id