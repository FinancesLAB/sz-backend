from sqlalchemy import select
from shared.models.asset import Asset
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.asset import AssetCreateAdm, AssetUpdateAdm
class AssetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj_in: AssetCreateAdm):
        obj=Asset(**obj_in.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)    
        return obj
    
    async def get_all(self):
        query = select(Asset)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, asset_id: int):
        query = select(Asset).where(Asset.id == asset_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def update(self, asset: Asset, obj_in: AssetUpdateAdm):
        update_data=obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(asset, field, value)
        await self.session.commit()
        await self.session.refresh(asset)
        return asset
    
    async def delete(self, asset: Asset):
        await self.session.delete(asset)
        await self.session.commit()
    
    async def get_by_ticker(self, ticker: str):
        query = select(Asset).where(Asset.ticker == ticker)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_assets_by_ids(self, ids: list[int]) -> dict[int, Asset]:
        query = select(Asset).where(Asset.id.in_(ids))
        result = await self.session.execute(query)
        rows = result.scalars().all()
        return rows