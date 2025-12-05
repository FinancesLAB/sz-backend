import asyncio
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.database import async_session_maker
from price_updater.services.asset_registry import AssetRegistry
from price_updater.config import UPDATE_INTERVAL
from price_updater.services.service import PricesService

asset_registry = AssetRegistry()

async def reload_assets():
    """Обновление списка активов каждые N минут."""
    async with async_session_maker() as session:
        await asset_registry.load(session)


async def job():
    """Основная задача — обновление цен для всех активов."""
    async with async_session_maker() as session:
        service = PricesService(session)
        await service.update_prices(asset_registry)


async def main():
    logger.info("Price Updater старт")

    await reload_assets()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=UPDATE_INTERVAL)
    scheduler.add_job(reload_assets, "interval", minutes=10)
    scheduler.start()
    await job()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())