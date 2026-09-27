import ConversationListItem from "./ConversationListItem";

/**
 * The saved-conversations list. Fixed column on desktop; a slide-in
 * drawer (with backdrop) on mobile, controlled by `isOpen`/`onClose`.
 */
export default function ConversationSidebar({
  conversations,
  activeConversationId,
  isLoading,
  onSelect,
  onNew,
  onDelete,
  isOpen,
  onClose,
}) {
  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 z-20 bg-ink/30 sm:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-30 flex w-72 shrink-0 flex-col border-r border-border bg-paper transition-transform duration-200 sm:static sm:z-auto sm:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="p-3">
          <button
            type="button"
            onClick={onNew}
            className="flex w-full items-center gap-2 rounded-xl border border-border bg-surface px-3 py-2 text-sm font-medium text-ink transition hover:bg-moss-light"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-4 w-4"
            >
              <path d="M12 5v14M5 12h14" />
            </svg>
            New chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-2 pb-3">
          {isLoading && (
            <p className="px-2 py-2 text-xs text-slate">Loading conversations…</p>
          )}

          {!isLoading && conversations.length === 0 && (
            <p className="px-2 py-2 text-xs text-slate">
              No conversations yet — start typing below.
            </p>
          )}

          {conversations.map((conversation) => (
            <ConversationListItem
              key={conversation.id}
              conversation={conversation}
              isActive={conversation.id === activeConversationId}
              onSelect={() => onSelect(conversation.id)}
              onDelete={() => onDelete(conversation.id)}
            />
          ))}
        </div>
      </aside>
    </>
  );
}