"use client";

import { useDevice } from "../context/DeviceContext";

export default function Sidebar({ devices }) {
  const { selectedDevice, setSelectedDevice } = useDevice();

  return (
    <aside className="w-64 bg-white border-r shadow-lg p-6 flex-shrink-0">
      <h1 className="text-xl font-bold mb-8">SocialBoost</h1>

      <nav className="flex flex-col gap-4">
        <a href="/" className="hover:text-blue-500">Dashboard</a>
        <a href="/send-token" className="hover:text-blue-500">Send Token</a>
        <a href="/settings" className="hover:text-blue-500">Settings</a>

        <h2 className="mt-6 font-semibold">Devices</h2>
        {devices.length === 0 ? (
          <p className="text-gray-500 text-sm mt-2">No devices found</p>
        ) : (
          devices.map((device) => (
            <button
              key={device.id}
              onClick={() => setSelectedDevice(device.id)}
              className={`text-left w-full text-sm mt-1 px-2 py-1 rounded ${
                selectedDevice === device.id
                  ? "bg-blue-200 font-semibold"
                  : device.status === "online"
                  ? "text-green-600"
                  : "text-red-600"
              } hover:bg-blue-100`}
            >
              {device.name} - {device.status}
            </button>
          ))
        )}
      </nav>
    </aside>
  );
}
