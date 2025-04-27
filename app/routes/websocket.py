from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from sqlalchemy.orm import Session

from app.config import get_db
from app.services.mahasiswa_service import get_detail_mahasiswa
from app.websockets.websocket_manager import WebSocketManager
from app.utils.dependencies import decode_jwt_token

from fastapi import HTTPException
from uuid import uuid4

router = APIRouter()
manager = WebSocketManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()

    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        user_id = decode_jwt_token(token)
        # Don't use Depends directly as shown below:
        # db: Session = Depends(get_db)  <- This is wrong
        # Instead, get the db from the function parameters as shown above
        mahasiswa = get_detail_mahasiswa(db, user_id)
        if mahasiswa:
            user_id = mahasiswa.nim
        else:
            await websocket.close(code=1008)
            return

    except HTTPException:
        await websocket.close(code=1008)
        return
    
    await manager.connect_user(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_user(user_id, websocket)
        print(f"❌ Disconnected user: {user_id}")

@router.websocket("/ws/public")
async def websocket_public(websocket: WebSocket):
    await websocket.accept()
    anon_id = str(uuid4())  # optional: give them a random ID
    await manager.connect_user(anon_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_user(anon_id, websocket)

# 👉 Testing endpoint: user connect manual pakai user_id
@router.websocket("/ws/test/{user_id}")
async def websocket_test_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    await manager.connect_user(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_user(user_id, websocket)
        print(f"❌ Disconnected (testing) user: {user_id}")