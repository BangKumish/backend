# app/utils/websocket_manager.py
from typing import Dict
from typing import List
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(websocket)
        print(f"🟢 Connected to room '{room}'. Total: {len(self.rooms[room])}")

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.rooms and websocket in self.rooms[room]:
            self.rooms[room].remove(websocket)
            print(f"🔴 Disconnected from room '{room}'. Remaining: {len(self.rooms[room])}")
            if not self.rooms[room]:
                del self.rooms[room]

    async def send_message(self, user_id: str, message: str):
        websocket = self.active_connections.get(user_id, [])
        for ws in websocket:
            try:
                await ws.send_text(message)
            except Exception as e:
                print(f"⚠️ Failed to send to {user_id}: {e}")

    async def send_json(self, user_id: str, data: dict):
        websocket = self.active_connections.get(user_id, [])
        for ws in websocket:
            try:
                await ws.send_json(data)
            except Exception as e:
                print(f"⚠️ Failed to send JSON to {user_id}: {e}")

    async def send_personal_message(self, message: dict, client_id: str):
        websocket = self.active_connections.get(client_id, [])
        for ws in websocket:
            try:
                await ws.send_json(message)
            except Exception as e:
                print(f"⚠️ Failed to send JSON to {client_id}: {e}")

    async def broadcast(self, message: dict):
        print("📢 Broadcasting to:", sum(len(v) for v in self.active_connections.values()))
        for uid, websocket in self.active_connections.items():
            for ws in websocket:
                try:
                    await ws.send_json(message)
                except Exception as e:
                    print(f"❌ Failed to send to {uid}: {e}")

    async def broadcast_to_room(self, room: str, message: dict):
        connections = self.rooms.get(room, [])
        print(f"📢 Broadcasting to '{room}': {len(connections)} clients")
        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"❌ Failed sending to '{room}': {e}")

    async def broadcast_all(self, message: dict):
        print("🌐 Broadcasting to all rooms")
        for room in list(self.rooms.keys()):
            await self.broadcast_to_room(room, message)
