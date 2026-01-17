from sqlalchemy import select
from shared.models.asset_price import AssetPrice
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.asset_price import AssetPriceCreate
from datetime import datetime


class AssetPriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj_in: AssetPriceCreate) -> AssetPrice:
        obj = AssetPrice(**obj_in.dict())
        self.session.add(obj)
        return obj

    async def get_all(self) -> list[AssetPrice]:
        query = select(AssetPrice)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, asset_id: int) -> AssetPrice:
        query = select(AssetPrice).where(AssetPrice.asset_id == asset_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_prices_since(
        self, ids: list[int], since: datetime
    ) -> list[AssetPrice]:
        if not ids:
            return []
        query = select(AssetPrice).where(
            AssetPrice.asset_id.in_(ids), AssetPrice.timestamp >= since
        )
        prices = await self.session.execute(query)
        return prices.scalars().all()

    async def get_last_price_by_id(self, asset_id: int) -> float | None:
        query = (
            select(AssetPrice.price)
            .where(AssetPrice.asset_id == asset_id)
            .order_by(AssetPrice.timestamp.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_prices_dict_by_ids(self, asset_ids: list[int]) -> dict[int, float]:
        query = (
            select(AssetPrice.asset_id, AssetPrice.price)
            .distinct(AssetPrice.asset_id)
            .where(AssetPrice.asset_id.in_(asset_ids))
            .order_by(AssetPrice.asset_id, AssetPrice.timestamp.desc())
        )
        result = await self.session.execute(query)
        rows = result.all()
        return {asset_id: price for asset_id, price in rows}
