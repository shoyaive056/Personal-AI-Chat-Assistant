"""Plain-text extraction — trivial, but kept as its own tool so the
dispatcher in document_service.py treats all three formats uniformly."""


def extract_text(file_bytes: bytes) -> str:
    """Decode a .txt file's bytes to a string.

    Raises ValueError if the file isn't valid text (e.g. it's actually a
    binary file with a misleading .txt extension).
    """
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Could not read this file as text: {exc}") from exc

    text = text.strip()
    if not text:
        raise ValueError("This file appears to be empty.")

    return text