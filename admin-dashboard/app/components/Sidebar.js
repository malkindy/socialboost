"use client";

import { useDevice } from "../context/DeviceContext";

export default function Sidebar() {
  const { devices, selectedDevice, setSelectedDevice } = useDevice();

  return (
    <aside className="w-64 bg-white border-r shadow-lg p-6 flex-shrink-0">
      <h1 className="text-xl font-bold mb-8">SocialBoost</h1>

      <nav className="flex flex-col gap-4">
        <a href="/" className="hover:text-blue-500">Dashboard</a>
        <a href="/send-token" className="hover:text-blue-500">Send Token</a>
        <a href="/settings" className="hover:text-blue-500">Settings</a>

        {/* Dropdown */}
        <h2 className="mt-6 font-semibold">Select Device</h2>

        {devices.length === 0 ? (
          <p className="text-gray-500 text-sm mt-2">No devices found</p>
        ) : (
          <select
            className="mt-2 p-2 border rounded bg-white"
            value={selectedDevice || ""}
            onChange={(e) => setSelectedDevice(e.target.value)}
          >
            <option value="">-- Select Device --</option>
            {devices.map((device) => (
              <option key={device.id} value={device.id}>
                {device.name} ({device.status})
              </option>
            ))}
          </select>
        )}
      </nav>
    </aside>
  );
}
