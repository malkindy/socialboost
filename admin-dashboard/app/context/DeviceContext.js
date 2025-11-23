"use client";

import { createContext, useContext, useState } from "react";

const DeviceContext = createContext();

export function DeviceProvider({ children }) {
  const [selectedDevice, setSelectedDevice] = useState(null);

  return (
    <DeviceContext.Provider value={{ selectedDevice, setSelectedDevice }}>
      {children}
    </DeviceContext.Provider>
  );
}

export function useDevice() {
  return useContext(DeviceContext);
}
