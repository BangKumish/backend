from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets.websocket_manager import WebSocketManager
from app.utils.dependencies import decode_jwt_token

from fastapi import HTTPException

router = APIRouter()
manager = WebSocketManager()
connected_client = []

@router.websocket("/ws/room/{room_name}")
async def websocket_room_endpoint(websocket: WebSocket, room_name: str):
    await manager.connect(websocket, room_name)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_name)

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📨 Received from {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        print(f"❌ Disconnected: {client_id}")

@router.websocket("/ws/layanan/{user_id}")
async def layanan_ws(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(user_id)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return
    
    try:
        user_id = decode_jwt_token(token)
    
    except HTTPException:
        await websocket.close(code=1008)
        return

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(user_id)
