import { useCallback, useState } from "react";
import ChatWindow from "../components/chat/ChatWindow";
import MessageInput from "../components/chat/MessageInput";
import ErrorMessage from "../components/chat/ErrorMessage";
import AttachedDocuments from "../components/chat/AttachedDocuments";
import ConversationSidebar from "../components/conversations/ConversationSidebar";
import { useChat } from "../hooks/useChat";
import { useConversations } from "../hooks/useConversations";

export default function ChatPage() {
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const {
    conversations,
    isLoading: isConversationsLoading,
    refresh: refreshConversations,
    removeConversation,
  } = useConversations();

  const handleConversationSaved = useCallback(
    (conversationId) => {
      setActiveConversationId(conversationId);
      refreshConversations();
    },
    [refreshConversations]
  );

  const {
    messages,
    documents,
    isLoading,
    isUploadingDocument,
    error,
    sendMessage,
    attachDocument,
    removeDocument,
    dismissError,
  } = useChat(activeConversationId, { onConversationSaved: handleConversationSaved });

  const handleNewConversation = () => {
    setActiveConversationId(null);
    setIsSidebarOpen(false);
  };

  const handleSelectConversation = (conversationId) => {
    setActiveConversationId(conversationId);
    setIsSidebarOpen(false);
  };

  const handleDeleteConversation = async (conversationId) => {
    await removeConversation(conversationId);
    if (conversationId === activeConversationId) {
      setActiveConversationId(null);
    }
  };

  return (
    <div className="flex flex-1 overflow-hidden">
      <ConversationSidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        isLoading={isConversationsLoading}
        onSelect={handleSelectConversation}
        onNew={handleNewConversation}
        onDelete={handleDeleteConversation}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />

      <div className="flex flex-1 flex-col overflow-hidden">
        <div className="flex shrink-0 items-center border-b border-border px-4 py-2 sm:hidden">
          <button
            type="button"
            onClick={() => setIsSidebarOpen(true)}
            aria-label="Open conversations"
            className="rounded-lg p-1.5 text-ink transition hover:bg-moss-light"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-5 w-5"
            >
              <path d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        <ChatWindow messages={messages} isLoading={isLoading} />

        <div className="shrink-0 px-4 pb-4 sm:px-0">
          {error && (
            <div className="mb-3">
              <ErrorMessage message={error} onDismiss={dismissError} />
            </div>
          )}
          <div className="mx-auto w-full max-w-[720px]">
            <AttachedDocuments
              documents={documents}
              isUploading={isUploadingDocument}
              onRemove={removeDocument}
            />
            <MessageInput
              onSend={sendMessage}
              onAttachFile={attachDocument}
              isUploadingDocument={isUploadingDocument}
              disabled={isLoading}
            />
          </div>
        </div>
      </div>
    </div>
  );
}