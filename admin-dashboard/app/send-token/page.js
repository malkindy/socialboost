"use client";

import { useState } from "react";
import { useDevice } from "../context/DeviceContext";

export default function SendTokenPage() {
  const { selectedDevice } = useDevice();
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const sendToken = async () => {
    if (!selectedDevice) {
      alert("Please select a device first");
      return;
    }

    setLoading(true);
    setResponse(null);

    try {
      const res = await fetch(
        `http://192.168.1.113:8000/api/send-token/${selectedDevice}`,
        { method: "POST" }
      );

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error("Failed to send token:", err);
      setResponse({ error: "Network error" });
    }

    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold">Send Token</h1>

      {/* Selected device */}
      <p className="mt-4">
        Selected Device:{" "}
        {selectedDevice ? (
          <span className="font-bold text-green-600">{selectedDevice}</span>
        ) : (
          <span className="text-red-500">None selected</span>
        )}
      </p>

      {/* Button */}
      <button
        onClick={sendToken}
        disabled={!selectedDevice || loading}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded disabled:bg-gray-400"
      >
        {loading ? "Sending..." : "Send Token to Device"}
      </button>

      {/* Show response */}
      {response && (
        <div className="mt-8 p-6 bg-white shadow rounded border">
          <h2 className="text-xl font-semibold mb-4">Token Sent!</h2>

          {/* Token text */}
          <p className="mb-4">
            <strong>Token:</strong> {response.token}
          </p>

          {/* QR Code Visual */}
          {response.qr_base64 && (
            <div className="mt-4">
              <h3 className="text-lg font-semibold mb-2">QR Code</h3>
              <img
                src={`data:image/png;base64,${response.qr_base64}`}
                alt="QR Code"
                className="w-64 h-64 border shadow rounded"
              />
            </div>
          )}

          {/* JSON */}
          <pre className="mt-6 p-4 bg-gray-100 rounded text-sm overflow-auto">
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
