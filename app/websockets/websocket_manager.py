# app/utils/websocket_manager.py
from typing import Dict
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print("Client connected! Total:", len(self.active_connections))

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"❌ Disconnected: {user_id} (Remaining: {len(self.active_connections)})")

    async def send_message(self, user_id: str, message: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)
        else:
            print(f"⚠️ User {user_id} not connected")

    async def send_personal_message(self, message: dict, client_id: str):
        websocket = self.active_connections.get(client_id)
        if websocket:
            await websocket.send_json(message)
        else:
            print(f"❌ Client {client_id} not connected")

    async def broadcast(self, message: dict):
        print("📢 Broadcasting to:", len(self.active_connections))
        for uid, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"❌ Failed to send to {uid}: {e}")
