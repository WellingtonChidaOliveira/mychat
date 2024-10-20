import ToggleButton from "./toggleButton";
import DownloadButton from "./downloadButton";
import OldChat from "./oldChats";
import { useEffect, useState } from "react";

type SidebarProps = {
  toggleSidebar: () => void;
  onSelectChat: (chatId: string) => void;
};

const SideBar = ({ toggleSidebar, onSelectChat }: SidebarProps) => {
  const [oldChats, setOldChats] = useState<{ id: string; title: string }[]>([]);

  // Fetch old chats from the backend when the sidebar is opened
  useEffect(() => {
    const fetchOldChats = async () => {
      const token = localStorage.getItem('token'); // Recupera o token do localStorage
      const response = await fetch(`http://localhost:8000/chat/`, {
        headers: {
          'authorization': `Bearer ${token}`, // Adiciona o token no cabeçalho
        },
      });
      const data = await response.json();
      setOldChats(data);
    };

    fetchOldChats();
  }, []);

  return (
    <div className="bg-zinc-800 h-full p-4 w-72 rounded-r-[10px] flex flex-col">
      <div className="flex justify-between">
        <ToggleButton toggleSidebar={toggleSidebar} className="hover:bg-zinc-600 rounded-md p-2"/>
        <DownloadButton className="hover:bg-zinc-600 rounded-md p-2"/>
      </div>

      <h2 className="text-white text-lg mb-4 mt-2">Histórico de Conversas</h2>
      <ul className="flex-1 overflow-y-auto">
        {oldChats.map(chat => (
          <OldChat key={chat.id} tittle={chat.title} onClick={() => onSelectChat(chat.id)} />
        ))}
      </ul>
    </div>
  );
};

export default SideBar;