"use client";

import { ReactNode, useState } from "react";
import Header from "../../components/header";
import SideBar from "../../components/sideBar";
import React from "react";

export default function ChatLayout({ children }: { children: ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSelectChat = (chatId: string) => {
    setCurrentChatId(chatId);
    setIsSidebarOpen(false); // Fechar a sidebar após selecionar um chat
  };

  return (
    <div className="w-screen h-screen flex">
      {isSidebarOpen && <SideBar toggleSidebar={toggleSidebar} onSelectChat={handleSelectChat} />}
      <div className="mx-auto grid h-screen w-full max-w-[1600px] grid-rows-[auto,1fr] gap-2 py-4">
        <Header isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
        <div className="flex w-full h-full flex-1 overflow-y-auto">  
          <div className="flex flex-grow h-full justify-center">
            {React.cloneElement(children as React.ReactElement, { currentChatId })}
          </div>
        </div>
      </div>
    </div>
  );
}