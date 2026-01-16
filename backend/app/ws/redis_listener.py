import asyncio
import redis.asyncio as redis
from app.core.config import settings
from app.ws.manager import ws_manager

async def redis_prices_listener(r: redis.Redis) -> None:
    pubsub = r.pubsub()
    await pubsub.subscribe(settings.REDIS_PRICES_CHANNEL)

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
            await pubsub.unsubscribe(settings.REDIS_PRICES_CHANNEL)
        finally:
            await pubsub.close()