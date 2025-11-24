"use client";

import { createContext, useContext, useState, useEffect } from "react";

const DeviceContext = createContext();

export function DeviceProvider({ children }) {
  const [devices, setDevices] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState(null);

  useEffect(() => {
    fetch("http://192.168.1.113:8000/api/devices/")
      .then((res) => res.json())
      .then((data) => setDevices(data))
      .catch((err) => console.error("Failed to fetch devices:", err));
  }, []);

  return (
    <DeviceContext.Provider value={{ devices, selectedDevice, setSelectedDevice }}>
      {children}
    </DeviceContext.Provider>
  );
}

export function useDevice() {
  return useContext(DeviceContext);
}
