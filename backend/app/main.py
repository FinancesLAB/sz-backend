import asyncio
from typing import Set

import redis.asyncio as redis
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.public import routers as public_routers
from app.api.routers.adm import routers as admin_routers
from app.core.config import settings
from app.ws.manager import ws_manager

app = FastAPI()

@app.websocket("/ws/prices")
async def ws_prices(ws: WebSocket):
    await ws_manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)

REDIS_URL=settings.REDIS_URL
REDIS_PRICES_CHANNEL=settings.REDIS_PRICES_CHANNEL

async def redis_prices_listener() -> None:
    r = redis.from_url(REDIS_URL, decode_responses=True)
    pubsub = r.pubsub()

    await pubsub.subscribe(REDIS_PRICES_CHANNEL)

    try:
        async for msg in pubsub.listen():
            if msg.get("type") != "message":
                continue

            data = msg.get("data")
            if data is None:
                continue

            await ws_manager.broadcast(str(data))

    except asyncio.CancelledError:
        raise

    finally:
        try:
            try:
                await pubsub.unsubscribe(REDIS_PRICES_CHANNEL)
            finally:
                await pubsub.close()
        finally:
            await r.close()


@app.on_event("startup")
async def on_startup() -> None:
    app.state.redis_prices_task = asyncio.create_task(redis_prices_listener())

@app.on_event("shutdown")
async def on_shutdown() -> None:
    task = getattr(app.state, "redis_prices_task", None)
    if task is not None:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass



api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in public_routers:
    api_router.include_router(r)

# for r in admin_routers:
#     api_router.include_router(r)

app.include_router(api_router)