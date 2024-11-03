"use client"; 

import Image from "next/image"; // Importing the Next.js Image component for optimized images.
import { useRouter } from 'next/navigation'; // Importing the useRouter hook for navigation (corrected to use next/navigation).

export default function Header() {
  const router = useRouter(); // Using the useRouter hook to access client-side navigation.

  const handleLogout = () => {
    localStorage.removeItem('token'); // Removes the authentication token from localStorage.
    router.push('/auth'); // Redirects the user to the login page after logging out.
  };

  return (
    <div className="flex items-center justify-between px-4"> 
      {/* A container with flex layout to position items horizontally, with padding on the sides. */}
      
      <div className="flex gap-2">
        {/* Flex container with a small gap between the logo image and the title. */}
        <Image src="/logo.png" alt="logo" height={32} width={32} />
        {/* Displaying the logo image with specified dimensions. */}
        <h1 className="text-2xl"><b>LOGO</b></h1>
        {/* Displaying a bold title with large font size. */}
      </div>

      <div className="flex items-center hover:bg-zinc-800 rounded-md p-2">
        {/* Flex container for the logout button, with hover effects and padding. */}
        <button className="flex items-center gap-1" onClick={handleLogout}>
          {/* Logout button triggers handleLogout on click and has some spacing between the icon and the text. */}
          <Image src="/sign-out.svg" alt="sign-out" width={30} height={30} />
          {/* Displaying a sign-out icon. */}
          <span>Logout</span>
          {/* Text label for the button. */}
        </button>
      </div>
    </div>
  );
}
