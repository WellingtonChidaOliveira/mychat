"use client"; // This is used in Next.js to specify that the component is client-side

import { useEffect, useState } from "react"; 
import { useRouter } from "next/navigation"; // or 'next/router' depending on the Next.js version
import Chat from "../../components/chat"; // Import the Chat component

export default function Home() {
  const router = useRouter(); // Hook to navigate to other pages
  const [loading, setLoading] = useState(true); // Loading state to control the loading behavior

  useEffect(() => {
    const token = localStorage.getItem("token"); // Retrieve token from localStorage
    if (!token) {
      router.push("/auth"); // If there's no token, redirect to the authentication page
    } else {
      setLoading(false); // Set loading to false if token exists
    }
  }, [router]); // Run this effect whenever the router changes

  // While loading is true, don't render the main content
  if (loading) {
    return <div>Loading...</div>; // Placeholder for a more styled loading spinner or animation
  }

  return (
    <div className="bg-zinc-800 rounded-[10px] flex justify-center items-center w-[70%] h-full">
      <Chat/> {/* Renders the Chat component once loading is done */}
    </div>
  );
}
