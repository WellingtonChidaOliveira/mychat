"use client";

import { useState } from 'react';
import TextBar from './textBar';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSendMessage = async (message: string) => {
    if (message.trim() === '') return;

    const newMessage: Message = { role: 'user', content: message };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    const token = localStorage.getItem('token'); // Recupera o token do localStorage

    // Envia a mensagem para o backend
    try {
      const response = await fetch(`http://localhost:8000/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'authorization': `Bearer ${token}`, // Adiciona o token no cabeçalho
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      // Assume que a resposta do servidor é a mensagem do assistente
      const assistantMessage: Message = { role: 'assistant', content: data.response };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

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
      </div>
      <TextBar onSendMessage={handleSendMessage} />
    </div>
  );
};

export default Chat;
