from fastapi import APIRouter, WebSocket

ws_router = APIRouter(prefix="/ws")


# websocat ws://localhost:8000/ws/healthcheck
@ws_router.websocket("/healthcheck")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
