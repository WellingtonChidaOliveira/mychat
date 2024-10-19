"use client";

import { ReactNode, useState } from "react";
import Header from "../../components/header";
import SideBar from "../../components/sideBar";

export default function ChatLayout({ children }: { children: ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="w-screen h-screen flex">
      {isSidebarOpen && <SideBar toggleSidebar={toggleSidebar}/>}
      <div className="mx-auto grid h-screen w-full max-w-[1600px] grid-rows-[auto,1fr] gap-2 py-4">
        <Header isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
        <div className="flex w-full h-full flex-1 overflow-y-auto ">  
          <div className="flex flex-grow h-full justify-center">
            {children}
          </div>
        </div>
      </div>
    </div>
    
  );
}
