"use client";

import "./globals.css";
import { DeviceProvider } from "./context/DeviceContext";
import Sidebar from "./components/Sidebar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="h-screen flex bg-gray-100 text-gray-900">

        <DeviceProvider>
          <Sidebar />

          <main className="flex-1 p-10 overflow-auto">
            {children}
          </main>
        </DeviceProvider>

      </body>
    </html>
  );
}
