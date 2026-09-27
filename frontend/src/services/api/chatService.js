// Chat feature's API calls, isolated from the generic client and from any
// React state. Future features (summarization, document analysis, etc.)
// should get their own sibling file here rather than growing this one.

import { apiClient } from "./apiClient";

/**
 * Send the full message history to the backend and get the assistant's
 * next reply. Pass `conversationId` to keep saving into an existing
 * conversation, or omit it to let the backend start a new one.
 * @param {{role: 'user'|'assistant', content: string}[]} messages
 * @param {string|null} [conversationId]
 * @returns {Promise<{reply: string, model: string, conversation_id: string}>}
 */
export function sendChatMessage(messages, conversationId = null) {
  const payload = {
    messages: messages.map(({ role, content }) => ({ role, content })),
    conversation_id: conversationId,
  };
  return apiClient.post("/api/chat", payload);
}