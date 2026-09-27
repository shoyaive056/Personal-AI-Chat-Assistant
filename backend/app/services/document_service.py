"""
Document persistence and text extraction.

Dispatches to the right tool in `tools/` by file extension, stores the
extracted text, and builds the context string that gets injected into the
AI's prompt. All database access for documents lives here, the same way
`conversation_service.py` owns conversations — routes and `ChatService`
never touch the `Document` model directly.
"""

from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.models.document import Document
from app.tools import docx_reader, pdf_reader, txt_reader

_EXTRACTORS = {
    ".pdf": pdf_reader.extract_text,
    ".docx": docx_reader.extract_text,
    ".txt": txt_reader.extract_text,
}


class UnsupportedFileTypeError(ValueError):
    """Raised when the uploaded file's extension isn't one we can read."""


class DocumentService:
    """CRUD and text-extraction operations for uploaded documents."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def extract_text(self, filename: str, file_bytes: bytes) -> str:
        """Dispatch to the right extractor by file extension.

        Raises UnsupportedFileTypeError for extensions we don't handle, or
        ValueError (from the extractor itself) if the file can't be read.
        """
        extension = Path(filename).suffix.lower()
        extractor = _EXTRACTORS.get(extension)

        if extractor is None:
            supported = ", ".join(sorted(_EXTRACTORS))
            raise UnsupportedFileTypeError(
                f"Unsupported file type '{extension}'. Supported types: {supported}"
            )

        return extractor(file_bytes)

    def save_document(
        self, conversation_id: str, filename: str, text: str
    ) -> Document:
        """Store extracted text against a conversation, truncating it to
        `MAX_DOCUMENT_CHARS` so one huge document can't blow up every
        future prompt in this conversation.
        """
        truncated = text[: settings.max_document_chars]

        document = Document(
            conversation_id=conversation_id,
            filename=filename,
            content_text=truncated,
            char_count=len(truncated),
        )
        self._db.add(document)
        self._db.commit()
        self._db.refresh(document)
        return document

    def get_documents_for_conversation(self, conversation_id: str) -> list[Document]:
        return (
            self._db.query(Document)
            .filter(Document.conversation_id == conversation_id)
            .order_by(Document.uploaded_at)
            .all()
        )

    def get_document(self, document_id: str) -> Document | None:
        return self._db.query(Document).filter(Document.id == document_id).first()

    def delete_document(self, document_id: str) -> bool:
        document = self.get_document(document_id)
        if document is None:
            return False
        self._db.delete(document)
        self._db.commit()
        return True

    @staticmethod
    def build_context_text(documents: list[Document]) -> str | None:
        """Combine every document's text into one block for the system
        prompt, or None if there are no documents to add.
        """
        if not documents:
            return None

        sections = [
            f"--- Document: {document.filename} ---\n{document.content_text}"
            for document in documents
        ]
        return (
            "The user has uploaded the following document(s) for you to "
            "reference when answering. Use them when relevant; say so "
            "plainly if the answer isn't in them.\n\n" + "\n\n".join(sections)
        )