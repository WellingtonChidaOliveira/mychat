import ToggleButton from "./toggleButton";
import DownloadButton from "./downloadButton";
import OldChat from "./oldChats";

type SidebarProps = {
  toggleSidebar: () => void;
}

const SideBar= ({toggleSidebar}: SidebarProps) => {

  const setChat = () => {
    return
  }

  return (
    <div className="bg-zinc-800 h-full p-4 w-72 rounded-r-[10px] flex flex-col">
        <div className="flex justify-between">
            <ToggleButton toggleSidebar={toggleSidebar} className="hover:bg-zinc-600 rounded-md p-2"/>
            <DownloadButton className="hover:bg-zinc-600 rounded-md p-2"/>
        </div>

        <h2 className="text-white text-lg mb-4 mt-2">Histórico de Conversas</h2>
        <ul className="flex-1 overflow-y-auto">
            <OldChat tittle="Teste" onClick={setChat}/>
            <OldChat tittle="Teste" onClick={setChat}/>
            <OldChat tittle="Teste" onClick={setChat}/>
        </ul>
    </div>
  );
};

export default SideBar;
