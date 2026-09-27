// Conversation feature's API calls, isolated the same way chatService.js
// isolates the chat endpoint — routes/hooks never call apiClient directly.

import { apiClient } from "./apiClient";

/** @returns {Promise<{id: string, title: string, created_at: string, updated_at: string}[]>} */
export function listConversations() {
  return apiClient.get("/api/conversations");
}

/** @returns {Promise<{id: string, title: string, messages: {id: string, role: string, content: string}[]}>} */
export function getConversation(conversationId) {
  return apiClient.get(`/api/conversations/${conversationId}`);
}

/** @returns {Promise<null>} */
export function deleteConversation(conversationId) {
  return apiClient.delete(`/api/conversations/${conversationId}`);
}