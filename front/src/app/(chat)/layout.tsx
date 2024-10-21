"use client";

import { ReactNode, useState } from "react";
import Header from "../../components/header";
import React from "react";

export default function ChatLayout({ children }: { children: ReactNode }) {

  return (
    <div className="w-screen h-screen flex">
      <div className="mx-auto grid h-screen w-full max-w-[1600px] grid-rows-[auto,1fr] gap-2 py-4">
        <Header />
        <div className="flex w-full h-full flex-1 overflow-y-auto">  
          <div className="flex flex-grow h-full justify-center">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}