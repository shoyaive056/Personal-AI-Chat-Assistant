import { MESSAGE_ROLES } from "../../constants/config";

export default function MessageBubble({ role, content }) {
  const isUser = role === MESSAGE_ROLES.USER;

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-2.5 text-[15px] leading-relaxed ${
          isUser
            ? "bg-ink text-paper rounded-br-sm"
            : "bg-surface border border-border text-ink rounded-bl-sm"
        }`}
      >
        {content}
      </div>
    </div>
  );
}