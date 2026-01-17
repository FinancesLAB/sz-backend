import redis.asyncio as redis
from app.core.config import settings


def create_redis() -> redis.Redis:
    return redis.from_url(settings.REDIS_URL, decode_responses=True)


async def close_redis(r: redis.Redis) -> None:
    await r.close()
