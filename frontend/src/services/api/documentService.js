// Document feature's API calls, isolated the same way chatService.js and
// conversationService.js isolate their own endpoints.

import { apiClient } from "./apiClient";

/**
 * Upload a PDF, DOCX, or TXT file. Pass `conversationId` to attach it to
 * an existing conversation, or omit it to let the backend start a new
 * conversation (its id comes back in the response).
 * @param {File} file
 * @param {string|null} [conversationId]
 * @returns {Promise<{document: {id: string, filename: string, char_count: number, uploaded_at: string}, conversation_id: string}>}
 */
export function uploadDocument(file, conversationId = null) {
  const formData = new FormData();
  formData.append("file", file);
  if (conversationId) formData.append("conversation_id", conversationId);
  return apiClient.postForm("/api/documents/upload", formData);
}

/** @returns {Promise<null>} */
export function deleteDocument(documentId) {
  return apiClient.delete(`/api/documents/${documentId}`);
}