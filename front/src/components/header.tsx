"use client";

import Image from "next/image";
import ToggleButton from "./toggleButton";
import DownloadButton from "./downloadButton";
import { useRouter } from 'next/navigation'; // Corrigido para usar o hook useRouter corretamente

type HeaderProps = {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
}

export default function Header({ isSidebarOpen, toggleSidebar }: HeaderProps) {
  const router = useRouter(); // Usar o hook useRouter no client-side

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove o token do localStorage
    router.push('/auth'); // Redireciona para a página de login
  };

  return (
    <div className="flex items-center justify-between px-4">
      {!isSidebarOpen ? (
        <div className="flex items-center gap-2">
          <ToggleButton toggleSidebar={toggleSidebar} className="hover:bg-zinc-800 rounded-md p-2" />
          <DownloadButton className="hover:bg-zinc-800 rounded-md p-2" />
        </div>
      ) : null}

      <div className="flex gap-2">
        <Image src="/logo.png" alt="logo" height={32} width={32} />
        <h1 className="text-2xl"><b>LOGO</b></h1>
      </div>

      <div className="flex items-center hover:bg-zinc-800 rounded-md p-2">
        <button className="flex items-center gap-1" onClick={handleLogout}>
          <Image src="/sign-out.svg" alt="sign-out" width={30} height={30} />
          <span>Sair</span>
        </button>
      </div>
    </div>
  );
}
