import Chat from "../../components/chat";

interface PageProps {
  currentChatId: string | null; // Recebendo o chatId
}

export default function Home({ currentChatId }: PageProps) {
  return (
    <div className="bg-zinc-800 rounded-[10px] flex justify-center items-center w-[70%] h-full">
      <Chat currentChatId={currentChatId} />
    </div>
  );
}