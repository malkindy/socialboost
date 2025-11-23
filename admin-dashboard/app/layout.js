"use client";

import './globals.css';
import { useEffect, useState } from "react";
import { DeviceProvider } from "./context/DeviceContext";
import Sidebar from "./components/Sidebar";

export default function RootLayout({ children }) {
  const [devices, setDevices] = useState([]);

  // Fetch devices
  useEffect(() => {
    fetch("http://192.168.1.113:8000/api/devices/")
      .then((res) => res.json())
      .then((data) => setDevices(data))
      .catch((err) => console.error("Failed to fetch devices:", err));
  }, []);

  return (
    <html lang="en">
      <body className="h-screen flex bg-gray-100 text-gray-900">
        <DeviceProvider>
          <Sidebar devices={devices} />
          <main className="flex-1 p-10 overflow-auto">
            {children}
          </main>
        </DeviceProvider>
      </body>
    </html>
  );
}
