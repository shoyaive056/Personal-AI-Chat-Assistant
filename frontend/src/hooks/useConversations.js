import { useCallback, useEffect, useState } from "react";
import {
  listConversations,
  deleteConversation,
} from "../services/api/conversationService";

/**
 * Owns the sidebar's list of saved conversations: fetching, refreshing
 * after a chat is saved, and deleting. Mirrors useChat's role, but for the
 * conversation list rather than a single conversation's messages.
 */
export function useConversations() {
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    try {
      const data = await listConversations();
      setConversations(data);
      setError(null);
    } catch (err) {
      setError(err.message || "Could not load conversations.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const removeConversation = useCallback(async (conversationId) => {
    await deleteConversation(conversationId);
    setConversations((current) =>
      current.filter((conversation) => conversation.id !== conversationId)
    );
  }, []);

  return { conversations, isLoading, error, refresh, removeConversation };
}