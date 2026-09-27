export default function ConversationListItem({
  conversation,
  isActive,
  onSelect,
  onDelete,
}) {
  const handleDelete = (event) => {
    event.stopPropagation();
    onDelete();
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onSelect}
      onKeyDown={(event) => event.key === "Enter" && onSelect()}
      className={`group mb-1 flex cursor-pointer items-center justify-between gap-2 rounded-lg px-3 py-2 text-sm transition ${
        isActive ? "bg-moss-light text-ink" : "text-ink/80 hover:bg-moss-light/60"
      }`}
    >
      <span className="truncate">{conversation.title}</span>

      <button
        type="button"
        onClick={handleDelete}
        aria-label="Delete conversation"
        className="shrink-0 text-slate opacity-0 transition hover:text-rust focus-visible:opacity-100 group-hover:opacity-100"
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
          <path d="M3 6h18" />
          <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
          <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
        </svg>
      </button>
    </div>
  );
}