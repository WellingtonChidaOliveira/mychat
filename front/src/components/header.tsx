"use client";

import Image from "next/image";
import { useRouter } from 'next/navigation'; // Corrigido para usar o hook useRouter corretamente

export default function Header() {
  const router = useRouter(); // Usar o hook useRouter no client-side

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove o token do localStorage
    router.push('/auth'); // Redireciona para a página de login
  };

  return (
    <div className="flex items-center justify-between px-4">
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
