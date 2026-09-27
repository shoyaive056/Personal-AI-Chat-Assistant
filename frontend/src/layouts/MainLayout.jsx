import TopBar from "../components/layout/TopBar";
import Watermark from "../components/layout/Watermark";

export default function MainLayout({ children }) {
  return (
    <div className="relative flex h-screen flex-col bg-paper">
      <Watermark />
      <div className="relative z-10 flex h-full flex-col">
        <TopBar />
        <main className="flex flex-1 flex-col overflow-hidden">{children}</main>
      </div>
    </div>
  );
}