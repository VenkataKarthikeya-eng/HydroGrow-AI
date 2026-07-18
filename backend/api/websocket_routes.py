from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from backend.authentication.jwt_handler import decode_token
from backend.database.connection import SessionLocal
from backend.database import crud
from typing import Dict, List

router = APIRouter()

class ConnectionManager:
    """
    Manages active user WebSocket sockets, facilitating authenticated live data broadcasts.
    """
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def broadcast_to_user(self, user_id: int, message: dict):
        if user_id in self.active_connections:
            for connection in list(self.active_connections[user_id]):
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(user_id, connection)

    async def broadcast_farm_intelligence_update(self, user_id: int, farm_score: float = 91.4, recommendations: list = None):
        payload = {
            "type": "farm_intelligence_update",
            "farm_score": farm_score,
            "recommendations": recommendations or [
                {"title": "DLI Target Met", "action": "Maintain LED dimming schedule"}
            ]
        }
        await self.broadcast_to_user(user_id, payload)

# Singleton manager
ws_manager = ConnectionManager()

@router.websocket("/ws/iot/live")
async def websocket_iot_live(websocket: WebSocket, token: str = Query(...)):
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=4001)
        return

    user_id = payload.get("user_id")
    if not user_id:
        await websocket.close(code=4001)
        return

    db = SessionLocal()
    user = crud.get_user(db, user_id=user_id)
    db.close()
    
    if not user:
        await websocket.close(code=4001)
        return

    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            # Hold loop open to accept messages / keepalive checks
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, websocket)
