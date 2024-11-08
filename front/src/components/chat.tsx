"use client";

import { useState } from 'react';
import TextBar from './textBar';
import ReactMarkdown from 'react-markdown';

// Define the type Message with two properties: role and content.
type Message = {
  role: 'user' | 'assistant'; // 'role' indicates whether the message is from the user or the assistant
  content: string; // 'content' holds the message text
};

// The Chat component manages the message list and handles sending messages.
const Chat = () => {
  // Use the useState hook to manage the state of messages. Initially, it is an empty array.
  const [messages, setMessages] = useState<Message[]>([]);

  // Function to handle sending a message. It's async because it sends a request to the backend.
  const handleSendMessage = async (message: string) => {
    // If the message is just empty spaces, it returns without doing anything.
    if (message.trim() === '') return;

    // Create a new message object with the user's message and update the message state.
    const newMessage: Message = { role: 'user', content: message };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    // Retrieve the token stored in localStorage, typically used for authentication.
    const token = localStorage.getItem('token'); // Retrieves the token from localStorage

    // Send the user's message to the backend server
    try {
      const response = await fetch(`http://localhost:8000/chat/ws`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Adds the Content-Type header to specify JSON format
          'authorization': `${token}`, // Adds the token in the authorization header
        },
        body: JSON.stringify({ payload: message }), // Sends the message as payload to the backend
      });

      // If the response is not OK (status code 200-299), throw an error.
      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      // Parse the JSON response from the backend.
      const data = await response.json();
      const resposta = JSON.parse(data.assistant);
      // Logs the response data (for debugging purposes)
      console.log(data)
      // Create a new assistant message using the content from the server response.
      const assistantMessage: Message = { role: 'assistant', content: resposta.Resposta};
      // Update the message state to include the assistant's response.
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      // If there's an error during the request, log it in the console.
      console.error('Error sending message:', error);
    }
  };
  return (
    <div className="flex flex-col h-full w-full p-4">
      {/* This div contains all the messages and scrolls automatically when there are too many */}
      <div className="flex-grow flex-1 overflow-y-auto pb-[16px]">
        {/* Map through the messages array and display each message */}
        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-2 my-2 w-fit max-w-prose break-words whitespace-pre-wrap ${
              message.role === 'user' // If it's the user's message, style it differently
                ? 'bg-[#3ea59f] text-white self-end ml-auto' // User messages: right-aligned with specific colors
                : 'bg-gray-300 text-black self-start mr-auto' // Assistant messages: left-aligned with specific colors
            } rounded-lg`}>
            {message.role === 'assistant' ? (
              <ReactMarkdown>{message.content}</ReactMarkdown> // Render assistant's messages as Markdown
            ) : (
              message.content // Render user's messages as plain text
            )}
          </div>
        ))}
      </div>
      {/* TextBar component where the user types their message */}
      <TextBar onSendMessage={handleSendMessage} />
    </div>
  );
};

export default Chat;
