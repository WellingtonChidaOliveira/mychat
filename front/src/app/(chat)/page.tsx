"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation"; // ou 'next/router' dependendo da versão
import Chat from "../../components/chat";

interface PageProps {
  currentChatId: string | null; // Recebendo o chatId
}

export default function Home({ currentChatId }: PageProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(true); // Estado de carregamento

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth");
    } else {
      setLoading(false); // Define o carregamento como falso se o token existir
    }
  }, [router]);

  // Enquanto o estado de carregamento estiver verdadeiro, não renderize o conteúdo
  if (loading) {
    return <div>Loading...</div>; // Você pode substituir isso por um carregador mais estilizado
  }

  return (
    <div className="bg-zinc-800 rounded-[10px] flex justify-center items-center w-[70%] h-full">
      <Chat currentChatId={currentChatId} />
    </div>
  );
}
