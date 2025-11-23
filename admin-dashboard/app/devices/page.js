"use client";

import { useState, useEffect } from "react";

export default function DevicesPage() {
  const [devices, setDevices] = useState([]);
  const [loadingDevices, setLoadingDevices] = useState(true);
  const [deviceQrs, setDeviceQrs] = useState({});
  const [loadingToken, setLoadingToken] = useState({});
  const [errorToken, setErrorToken] = useState({});
  const [errorDevices, setErrorDevices] = useState(null);

  // Fetch devices from backend
  useEffect(() => {
    const fetchDevices = async () => {
      setLoadingDevices(true);
      setErrorDevices(null);

      try {
        const res = await fetch("http://192.168.1.113:8000/api/devices");
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        const data = await res.json();
        setDevices(data);
      } catch (err) {
        console.error(err);
        setErrorDevices("Failed to load devices");
      } finally {
        setLoadingDevices(false);
      }
    };

    fetchDevices();
  }, []);

  const handleSendToken = async (device) => {
    setLoadingToken((prev) => ({ ...prev, [device.id]: true }));
    setErrorToken((prev) => ({ ...prev, [device.id]: null }));

    try {
      const res = await fetch(
        `http://192.168.1.113:8000/api/send-token/${device.id}`,
        { method: "POST" }
      );

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setDeviceQrs((prev) => ({ ...prev, [device.id]: data.qr_base64 }));
    } catch (err) {
      console.error(err);
      setErrorToken((prev) => ({ ...prev, [device.id]: "Failed to send token" }));
    } finally {
      setLoadingToken((prev) => ({ ...prev, [device.id]: false }));
    }
  };

  if (loadingDevices) return <p className="p-6">Loading devices...</p>;
  if (errorDevices) return <p className="p-6 text-red-500">{errorDevices}</p>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Devices</h1>

      <table className="min-w-full bg-white border shadow">
        <thead>
          <tr className="bg-gray-100">
            <th className="py-2 px-4 border">ID</th>
            <th className="py-2 px-4 border">Name</th>
            <th className="py-2 px-4 border">Status</th>
            <th className="py-2 px-4 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          {devices.map((device) => (
            <tr key={device.id} className="text-center">
              <td className="py-2 px-4 border">{device.id}</td>
              <td className="py-2 px-4 border">{device.name}</td>
              <td className="py-2 px-4 border">
                <span
                  className={`px-2 py-1 rounded-full text-white text-sm ${
                    device.status === "online" ? "bg-green-500" : "bg-red-500"
                  }`}
                >
                  {device.status}
                </span>
              </td>
              <td className="py-2 px-4 border">
                <button
                  onClick={() => handleSendToken(device)}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                  disabled={loadingToken[device.id]}
                >
                  {loadingToken[device.id] ? "Sending..." : "Send Token"}
                </button>

                {errorToken[device.id] && (
                  <p className="text-red-500 mt-1">{errorToken[device.id]}</p>
                )}

                {deviceQrs[device.id] && (
                  <img
                    src={`data:image/png;base64,${deviceQrs[device.id]}`}
                    alt={`QR for ${device.name}`}
                    className="border p-2 mt-2 mx-auto"
                  />
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
