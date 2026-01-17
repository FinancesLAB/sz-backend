from loguru import logger
import aiohttp
from price_updater.clients.moex_client import MoexClient
from shared.repositories.asset_price import AssetPriceRepository
from app.schemas.asset_price import AssetPriceCreate
from app.core.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession


class PricesService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AssetPriceRepository

    async def update_prices(self, asset_registry):
        logger.info("****** Обновление цен *******")
        assets = asset_registry.get_all()
        if not assets:
            return
        prices = await MoexClient.get_all_prices()
        async with async_session_maker() as session:
            async with session.begin():
                repo = self.repo(session=session)
                for asset_id, ticker in assets.items():
                    price = prices.get(ticker)
                    if price is None:
                        continue
                    await repo.create(
                        AssetPriceCreate(
                            asset_id=asset_id,
                            price=price,
                            currency="RUB",
                            source="moex",
                        )
                    )
                    logger.info(f"💰 {ticker}: {price}")

        logger.info("****** Обновление завершено ******")
