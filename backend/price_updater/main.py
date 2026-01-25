import asyncio

from app.core.database import async_session_maker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from price_updater.clients.moex_client import MoexClient
from price_updater.config import UPDATE_INTERVAL
from price_updater.services.asset_registry import AssetRegistry
from price_updater.services.service import PricesService

asset_registry = AssetRegistry()
moex_client = MoexClient()


async def reload_assets():
    async with async_session_maker() as session:
        await asset_registry.load(session)


async def job():
    async with async_session_maker() as session:
        service = PricesService(session, moex_client)
        await service.update_prices(asset_registry)


async def main():
    await moex_client.aopen()
    try:
        await reload_assets()
        await job()

        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            job,
            'interval',
            seconds=UPDATE_INTERVAL,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=30,
        )
        scheduler.add_job(
            reload_assets,
            'interval',
            minutes=60,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=300,
        )

        scheduler.start()
        await asyncio.Event().wait()
    finally:
        await moex_client.aclose()


if __name__ == '__main__':
    asyncio.run(main())
