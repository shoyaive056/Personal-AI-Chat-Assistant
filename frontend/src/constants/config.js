// Central place for app-wide constant values. Anything that might need to
// change later (URLs, limits, copy used in more than one place) should live
// here instead of being hardcoded inside components.

export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const APP_NAME = "Shoyaive AI";

export const MESSAGE_ROLES = {
  USER: "user",
  ASSISTANT: "assistant",
};

// Kept in sync with the backend's default MAX_UPLOAD_SIZE_MB and the
// extensions supported by app/tools/*_reader.py.
export const ACCEPTED_DOCUMENT_TYPES = ".pdf,.docx,.txt";
export const MAX_DOCUMENT_SIZE_MB = 10;