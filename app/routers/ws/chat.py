import datetime
import json
from typing import Dict, List

from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.models import Message

ws_chat_router = APIRouter(prefix="/ws")

active_connections: Dict[int, List[WebSocket]] = {}


@ws_chat_router.websocket("/chat/{chat_id}")
async def chat_ws(
    websocket: WebSocket,
    chat_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    await websocket.accept()
    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            text = data_json.get("text")

            msg = Message(
                chat_id=chat_id,
                sender_id=user_id,
                text=text,
                timestamp=datetime.datetime.utcnow(),
                is_read=False,
            )
            db.add(msg)
            await db.commit()
            await db.refresh(msg)

            for conn in active_connections[chat_id]:
                await conn.send_json(
                    {
                        "id": msg.id,
                        "chat_id": chat_id,
                        "sender_id": user_id,
                        "text": text,
                        "timestamp": msg.timestamp.isoformat(),
                        "is_read": False,
                    }
                )
    except Exception as ex:
        print(f"Websoket error: {ex}")
    finally:
        active_connections[chat_id].remove(websocket)
