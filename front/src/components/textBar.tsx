// src/app/components/TextBar.tsx
import { useState } from "react";

interface TextBarProps {
  onSendMessage: (message: string) => void;
}

export default function TextBar({ onSendMessage }: TextBarProps) {
  const [input, setInput] = useState('');

  const handleSendClick = () => {
    if (input.trim() !== '') {  // Verifica se o input não está vazio
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendClick(); // Chama a função de envio ao pressionar "Enter"
    }
  };

  return (
    <div className="w-full flex justify-center items-center gap-2 justify-self-center">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown} // Adiciona o manipulador de eventos para a tecla "Enter"
        placeholder="Escreva a sua mensagem aqui"
        className="w-full rounded-[10px] px-4 py-3 bg-zinc-600 hover:bg-zinc-500 placeholder-gray-100"
      />
      <button
        className="px-5 py-2 rounded-[50px] bg-[#3ea59f] hover:bg-[#32847f] text-fuchsia-50"
        onClick={handleSendClick}
      >
        Send
      </button>
    </div>
  );
}
