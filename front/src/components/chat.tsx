"use client";

import { useEffect, useState } from 'react';
import TextBar from './textBar';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

type ChatProps = {
  currentChatId: string | null;
};

const Chat = ({ currentChatId }: ChatProps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [currentAssistantMessage, setCurrentAssistantMessage] = useState<string>('');
  const [chatId, setChatId] = useState<string | null>(currentChatId);

  useEffect(() => {
    // Se não houver chatId, cria um novo chat no backend
    const initializeChat = async () => {
      if (!chatId) {
        try {
          const response = await fetch('http://localhost:4000/chats', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          const data = await response.json();
          setChatId(data.id);  // Salvar o novo chatId gerado pelo backend
        } catch (error) {
          console.error("Erro ao criar novo chat:", error);
        }
      }
    };

    initializeChat();
  }, [chatId]);

  // Fetch mensagens e conectar ao WebSocket quando houver um chatId
  useEffect(() => {
    if (!chatId) return;

    const fetchMessages = async () => {
      const response = await fetch(`http://localhost:4000/chats/${chatId}/messages`);
      const data = await response.json();
      setMessages(data);
    };

    fetchMessages();
  }, [chatId]);

  useEffect(() => {
    if (!chatId) return;

    const socket = new WebSocket(`ws://localhost:4000/chats/${chatId}/ws`);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.role === 'assistant') {
        setCurrentAssistantMessage((prev) => prev + data.content);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket closed");
    };

    setWs(socket);

    return () => socket.close();
  }, [chatId]);

  const handleSendMessage = (message: string) => {
    if (!ws || message.trim() === '') return;

    const newMessage: Message = { role: 'user', content: message };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    ws.send(JSON.stringify({ message }));
  };

  useEffect(() => {
    if (currentAssistantMessage) {
      const timer = setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { role: 'assistant', content: currentAssistantMessage },
        ]);
        setCurrentAssistantMessage('');
      }, 1000);

      return () => clearTimeout(timer);
    }
  }, [currentAssistantMessage]);

  return (
    <div className="flex flex-col h-full w-full p-4">
      <div className="flex-grow flex-1 overflow-y-auto pb-[16px]">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-2 my-2 w-fit max-w-prose break-words whitespace-pre-wrap ${
              message.role === 'user'
                ? 'bg-[#3ea59f] text-white self-end ml-auto'
                : 'bg-gray-300 text-black self-start mr-auto'
            } rounded-lg`}>
            {message.content}
          </div>
        ))}

        {currentAssistantMessage && (
          <div className="p-2 my-2 w-fit max-w-prose break-words whitespace-pre-wrap bg-gray-300 text-black self-start mr-auto rounded-lg">
            {currentAssistantMessage}
          </div>
        )}
      </div>
      <TextBar onSendMessage={handleSendMessage} />
    </div>
  );
};

export default Chat;
