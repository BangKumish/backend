# app/utils/websocket_manager.py
from typing import Dict
from typing import List
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect_user(self, user_id: str, websocket: WebSocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"🟢 Connected user '{user_id}'. Total connections: {len(self.active_connections[user_id])}")

    def disconnect_user(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections and websocket in self.active_connections[user_id]:
            self.active_connections[user_id].remove(websocket)
            print(f"🔴 Disconnected user '{user_id}'. Remaining: {len(self.active_connections[user_id])}")
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: str):
        connections = self.active_connections.get(user_id, [])
        for ws in connections:
            try:
                await ws.send_text(message)
            except Exception as e:
                print(f"⚠️ Failed to send to {user_id}: {e}")

    async def send_json(self, user_id: str, data: dict):
        connections = self.active_connections.get(user_id, [])
        for ws in connections:
            try:
                await ws.send_json(data)
            except Exception as e:
                print(f"⚠️ Failed to send JSON to {user_id}: {e}")

    async def broadcast(self, message: dict):
        print("📢 Broadcasting to:", sum(len(v) for v in self.active_connections.values()))
        for user_id, connections in self.active_connections.items():
            for ws in connections:
                try:
                    await ws.send_json(message)
                except Exception as e:
                    print(f"❌ Failed to send to {user_id}: {e}")

    async def broadcast_all(self, message: dict):
        print("🌐 Broadcasting to all unique connections")
        unique_connections = set()

        for connections in self.active_connections.values():
            for ws in connections:
                unique_connections.add(ws)

        for ws in unique_connections:
            try:
                await ws.send_json(message)
            except Exception as e:
                print(f"❌ Failed to broadcast: {e}")

        print(f"✅ Broadcasted to {len(unique_connections)} unique connections")

