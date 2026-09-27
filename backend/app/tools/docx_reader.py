"""DOCX text extraction."""

from io import BytesIO

from docx import Document as DocxDocument
from docx.opc.exceptions import PackageNotFoundError


def extract_text(file_bytes: bytes) -> str:
    """Return all paragraph and table text from a .docx file, in order.

    Raises ValueError if the file isn't a readable .docx — callers turn
    that into a clean 4xx response.
    """
    try:
        document = DocxDocument(BytesIO(file_bytes))
    except PackageNotFoundError as exc:
        raise ValueError(f"Could not read this Word document: {exc}") from exc

    parts: list[str] = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            parts.append(paragraph.text.strip())

    for table in document.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if cells:
                parts.append(" | ".join(cells))

    text = "\n".join(parts)

    if not text:
        raise ValueError("No text could be extracted from this document.")

    return text