/**
 * Chips for documents attached to the current conversation, shown above
 * the message input. A document stays attached for the whole conversation
 * (per the backend's design — see chat_service.py) rather than just the
 * next message, so this list persists across turns and reloads.
 */
export default function AttachedDocuments({
  documents,
  isUploading,
  onRemove,
}) {
  if (documents.length === 0 && !isUploading) return null;

  return (
    <div className="mb-2 flex flex-wrap gap-2">
      {documents.map((document) => (
        <div
          key={document.id}
          className="flex items-center gap-1.5 rounded-full border border-border bg-surface py-1 pl-3 pr-1.5 text-xs text-ink"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="h-3.5 w-3.5 shrink-0 text-slate"
          >
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <path d="M14 2v6h6" />
          </svg>
          <span className="max-w-[160px] truncate">{document.filename}</span>
          <button
            type="button"
            onClick={() => onRemove(document.id)}
            aria-label={`Remove ${document.filename}`}
            className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-slate transition hover:bg-moss-light hover:text-ink"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-2.5 w-2.5"
            >
              <path d="M18 6 6 18M6 6l12 12" />
            </svg>
          </button>
        </div>
      ))}

      {isUploading && (
        <div className="flex items-center gap-1.5 rounded-full border border-border bg-surface py-1 pl-3 pr-3 text-xs text-slate">
          <span className="h-3 w-3 animate-spin rounded-full border-2 border-slate/30 border-t-slate" />
          Uploading…
        </div>
      )}
    </div>
  );
}