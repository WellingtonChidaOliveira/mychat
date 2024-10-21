import { useState } from "react";

interface TextBarProps {
  onSendMessage: (message: string) => void;  // Function passed as a prop to handle sending messages
}

export default function TextBar({ onSendMessage }: TextBarProps) {
  const [input, setInput] = useState('');  // Manages the text input state

  const handleSendClick = () => {
    if (input.trim() !== '') {  // Checks if the input is not empty
      onSendMessage(input);     // Sends the message through the passed function
      setInput('');             // Clears the input field after sending
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendClick(); // Calls the send function when the "Enter" key is pressed
    }
  };

  return (
    <div className="w-full flex justify-center items-center gap-2 justify-self-center">
      <input
        type="text"
        value={input}  // Binds the input state to the input field's value
        onChange={(e) => setInput(e.target.value)}  // Updates the input state on change
        onKeyDown={handleKeyDown}  // Adds an event listener for the "Enter" key
        placeholder="Type your message here"  // Placeholder text for the input
        className="w-full rounded-[10px] px-4 py-3 bg-zinc-600 hover:bg-zinc-500 placeholder-gray-100"
      />
      <button
        className="px-5 py-2 rounded-[50px] bg-[#3ea59f] hover:bg-[#32847f] text-fuchsia-50"
        onClick={handleSendClick}  // Calls the send function when the button is clicked
      >
        Send
      </button>
    </div>
  );
}
