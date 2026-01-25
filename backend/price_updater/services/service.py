from app.schemas.asset_price import AssetPriceCreate
from loguru import logger
from price_updater.clients.moex_client import MoexClient
from shared.repositories.asset_price import AssetPriceRepository
from sqlalchemy.ext.asyncio import AsyncSession


class PricesService:
    def __init__(self, session: AsyncSession, moex: MoexClient):
        self._db_session = session
        self._moex = moex
        self.repo = AssetPriceRepository

    async def update_prices(self, asset_registry):
        assets = asset_registry.get_all()
        if not assets:
            return
        prices = await self._moex.get_all_prices()
        async with self._db_session.begin():
            repo = self.repo(self._db_session)
            for asset_id, ticker in assets.items():
                price = prices.get(ticker)
                if price is None:
                    continue
                await repo.create(
                    AssetPriceCreate(asset_id=asset_id, price=price, currency='RUB', source='moex')
                )
                logger.info(f'💰 {ticker}: {price}')
