import { useCallback, useEffect, useRef, useState } from "react";
import { sendChatMessage } from "../services/api/chatService";
import { getConversation } from "../services/api/conversationService";
import { uploadDocument, deleteDocument } from "../services/api/documentService";
import { MESSAGE_ROLES, MAX_DOCUMENT_SIZE_MB } from "../constants/config";
import { generateId } from "../utils/id";

/**
 * Owns all state and logic for the active conversation: messages, loading
 * state, errors, and attached documents. Pages/components stay
 * presentational and just call `sendMessage` / `attachDocument`.
 *
 * @param {string|null} conversationId - the conversation to load and keep
 *   saving into. Pass `null` for a fresh, unsaved conversation.
 * @param {{onConversationSaved?: (conversationId: string) => void}} [options]
 *   `onConversationSaved` fires after every successful send or upload with
 *   the conversation's id (a new one the first time), so the caller can
 *   update its own state and refresh the sidebar list.
 */
export function useChat(conversationId, { onConversationSaved } = {}) {
  const [messages, setMessages] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploadingDocument, setIsUploadingDocument] = useState(false);
  const [error, setError] = useState(null);

  // Tracks which conversation's messages are currently loaded, so we don't
  // re-fetch a conversation we just loaded or just saved into.
  const loadedConversationId = useRef(null);

  useEffect(() => {
    if (!conversationId) {
      setMessages([]);
      setDocuments([]);
      loadedConversationId.current = null;
      return;
    }

    if (loadedConversationId.current === conversationId) return;

    let cancelled = false;
    setIsLoading(true);
    setError(null);

    getConversation(conversationId)
      .then((conversation) => {
        if (cancelled) return;
        setMessages(
          conversation.messages.map((m) => ({
            id: m.id,
            role: m.role,
            content: m.content,
          }))
        );
        setDocuments(conversation.documents);
        loadedConversationId.current = conversationId;
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message || "Could not load this conversation.");
        }
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [conversationId]);

  const sendMessage = useCallback(
    async (content) => {
      const trimmed = content.trim();
      if (!trimmed || isLoading) return;

      const userMessage = {
        id: generateId(),
        role: MESSAGE_ROLES.USER,
        content: trimmed,
      };

      const nextMessages = [...messages, userMessage];
      setMessages(nextMessages);
      setError(null);
      setIsLoading(true);

      try {
        const { reply, conversation_id: savedConversationId } =
          await sendChatMessage(nextMessages, conversationId);

        setMessages((current) => [
          ...current,
          { id: generateId(), role: MESSAGE_ROLES.ASSISTANT, content: reply },
        ]);

        // We already have these messages locally — mark this conversation
        // as loaded so the effect above doesn't re-fetch it.
        loadedConversationId.current = savedConversationId;
        onConversationSaved?.(savedConversationId);
      } catch (err) {
        setError(err.message || "Something went wrong. Please try again.");
      } finally {
        setIsLoading(false);
      }
    },
    [messages, isLoading, conversationId, onConversationSaved]
  );

  const attachDocument = useCallback(
    async (file) => {
      const maxBytes = MAX_DOCUMENT_SIZE_MB * 1024 * 1024;
      if (file.size > maxBytes) {
        setError(`"${file.name}" is too large. Maximum size is ${MAX_DOCUMENT_SIZE_MB} MB.`);
        return;
      }

      setIsUploadingDocument(true);
      setError(null);

      try {
        const { document, conversation_id: savedConversationId } =
          await uploadDocument(file, conversationId);

        setDocuments((current) => [...current, document]);

        // Uploading a document creates a conversation the same way
        // sending a first message does — adopt it the same way.
        loadedConversationId.current = savedConversationId;
        onConversationSaved?.(savedConversationId);
      } catch (err) {
        setError(err.message || "Could not upload the document.");
      } finally {
        setIsUploadingDocument(false);
      }
    },
    [conversationId, onConversationSaved]
  );

  const removeDocument = useCallback(async (documentId) => {
    try {
      await deleteDocument(documentId);
      setDocuments((current) => current.filter((doc) => doc.id !== documentId));
    } catch (err) {
      setError(err.message || "Could not remove the document.");
    }
  }, []);

  const dismissError = useCallback(() => setError(null), []);

  return {
    messages,
    documents,
    isLoading,
    isUploadingDocument,
    error,
    sendMessage,
    attachDocument,
    removeDocument,
    dismissError,
  };
}