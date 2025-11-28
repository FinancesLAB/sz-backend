from sqlalchemy import select
from shared.models.asset_price import AssetPrice
from datetime import datetime
class AssetPriceRepository:
    @staticmethod
    async def get_by_id(session, asset_id: int):
        query = select(AssetPrice).where(AssetPrice.asset_id == asset_id)
        result = await session.execute(query)
        asserts = result.scalars().all()
        return asserts
    
    @staticmethod
    async def get_all(session):
        query = select(AssetPrice)
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def create(session,
            asset_id,
            price,
            currency,
            source):
        new_price = AssetPrice(
            asset_id=asset_id,
            price=price,
            currency=currency,
            source=source
        )
        session.add(new_price)
        await session.commit()
        await session.refresh(new_price)
        return new_price
    
    @staticmethod
    async def get_prices_since(session, ids: list[int], since: datetime):
        if not ids: return []
        query = (select(AssetPrice).where(AssetPrice.asset_id.in_(ids), AssetPrice.timestamp >= since))
        prices = await session.execute(query)
        return prices.scalars().all()
    