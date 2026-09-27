export default function ErrorMessage({ message, onDismiss }) {
  if (!message) return null;

  return (
    <div className="mx-auto flex w-full max-w-[720px] items-start justify-between gap-3 rounded-xl border border-rust-border bg-rust-bg px-4 py-3 text-sm text-rust">
      <span>{message}</span>
      <button
        type="button"
        onClick={onDismiss}
        className="shrink-0 text-rust/70 transition hover:text-rust"
        aria-label="Dismiss error"
      >
        ✕
      </button>
    </div>
  );
}