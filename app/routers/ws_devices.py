# app/routers/ws_devices.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

# Store connected WebSocket clients
connected_clients: List[WebSocket] = []


@router.websocket("/ws/devices")
async def websocket_devices(websocket: WebSocket):
    """WebSocket for real-time device updates (online/offline)."""
    await websocket.accept()
    connected_clients.append(websocket)
    print("[WS] Client connected. Total:", len(connected_clients))

    try:
        while True:
            # We ignore any messages from client — this WS is push-only
            await websocket.receive_text()

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("[WS] Client disconnected. Total:", len(connected_clients))


async def broadcast_device_status(device_id: int, status: str):
    """
    Push update to all connected admin dashboards.
    Example:
      await broadcast_device_status(1, "online")
    """
    message = {"id": device_id, "status": status}

    print("[WS] Broadcasting:", message)

    for ws in connected_clients:
        await ws.send_json(message)
