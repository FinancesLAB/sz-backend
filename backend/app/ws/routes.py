from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from app.ws.manager import ws_manager

ws_router = APIRouter(prefix="/ws", tags=["Prices ws"])

@ws_router.websocket("/prices")
async def ws_prices(ws: WebSocket):
    await ws_manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)