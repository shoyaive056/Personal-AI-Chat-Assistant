import { APP_NAME } from "../../constants/config";

/**
 * A faint, fixed brand mark behind the chat content — gives the page some
 * texture beyond flat light/dark backgrounds without being a distraction.
 * Purely decorative: `aria-hidden`, `select-none`, and `pointer-events-none`
 * so it never interferes with reading or clicking anything above it.
 */
export default function Watermark() {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 z-0 flex select-none items-center justify-center overflow-hidden"
    >
      <span className="whitespace-nowrap rotate-[-12deg] font-serif text-[20vw] font-medium leading-none text-ink/[0.035]">
        {APP_NAME}
      </span>
    </div>
  );
}