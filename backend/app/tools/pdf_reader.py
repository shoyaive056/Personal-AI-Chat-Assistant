"""
PDF text extraction.

One focused function, no business logic — `document_service.py` decides
what to do with the extracted text (store it, truncate it, etc.). This is
the first thing under `tools/`, following the layout the project's
roadmap sketched out from the start.
"""

from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text(file_bytes: bytes) -> str:
    """Return all extractable text from a PDF, pages joined by blank lines.

    Raises ValueError if the file isn't a readable PDF (e.g. corrupted or
    password-protected) — callers turn that into a clean 4xx response.
    """
    try:
        reader = PdfReader(BytesIO(file_bytes))
    except PdfReadError as exc:
        raise ValueError(f"Could not read this PDF: {exc}") from exc

    if reader.is_encrypted:
        raise ValueError("This PDF is password-protected and can't be read.")

    pages_text = [page.extract_text() or "" for page in reader.pages]
    text = "\n\n".join(page.strip() for page in pages_text if page.strip())

    if not text:
        raise ValueError(
            "No text could be extracted from this PDF. It may be a "
            "scanned image without a text layer."
        )

    return text