import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import LoadingIndicator from "./LoadingIndicator";
import { APP_NAME } from "../../constants/config";

export default function ChatWindow({ messages, isLoading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center px-6 text-center">
        <p className="font-serif text-[28px] font-medium text-ink">
          What can I help with?
        </p>
        <p className="mt-2 max-w-sm text-sm text-slate">
          {APP_NAME} is a personal assistant, starting with conversation and
          growing from here.
        </p>
      </div>
    );
  }

  return (
    <div className="scroll-thin flex-1 overflow-y-auto px-4 py-6 sm:px-0">
      <div className="mx-auto flex w-full max-w-[720px] flex-col gap-4">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            role={message.role}
            content={message.content}
          />
        ))}
        {isLoading && <LoadingIndicator />}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
