from sqlalchemy import select
from backend.app.models.asset import Asset

class AssetRepository:
    @staticmethod
    async def get_all(session):
        query = select(Asset)
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(asset_id: int, session):
        query = select(Asset).where(Asset.id == asset_id)
        result = await session.execute(query)
        asset = result.scalar_one_or_none()
        return asset
    
    @staticmethod
    async def get_by_ticker(ticker: str, session):
        query = select(Asset).where(Asset.ticker == ticker)
        result = await session.execute(query)
        asset = result.scalar_one_or_none()
        return asset
    
    @staticmethod
    async def create(session, ticker: str, full_name: str, type: str):
        new_asset = Asset(
            ticker=ticker, 
            full_name=full_name,
            type=type
            )
        session.add(new_asset)
        await session.commit()
        await session.refresh(new_asset)
        return new_asset
    
    @staticmethod
    async def delete(session, asset: Asset):
        await session.delete(asset)
        await session.commit()

    
        
    @staticmethod
    async def update(session, asset: Asset, data: dict):
        for field, value in data.items():
            setattr(asset, field, value)
        await session.flush()
        return asset
    