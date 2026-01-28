from app.schemas.asset import AssetCreateAdm, AssetUpdateAdm
from fastapi import HTTPException
from app.repositories import AssetRepositoryPostgres
from sqlalchemy.ext.asyncio import AsyncSession


class AssetService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AssetRepositoryPostgres(session=session)

    async def get_all(self, *, limit: int, offset: int):
        items = await self.repo.get_all(limit=limit, offset=offset)
        total = await self.repo.count()
        return items, total

    async def get_by_id(self, asset_id: int):
        asset = await self.repo.get_by_id(asset_id=asset_id)
        if asset is None:
            raise HTTPException(404, 'SZ asset not found')
        return asset

    async def get_by_ticker(self, ticker: str):
        asset = await self.repo.get_by_ticker(ticker=ticker)
        if asset is None:
            raise HTTPException(404, 'SZ asset not found')
        return asset

    async def create(self, obj_in: AssetCreateAdm):
        return await self.repo.create(obj_in=obj_in)

    async def delete(self, asset_id: int):
        asset = await self.repo.get_by_id(asset_id=asset_id)
        if asset is None:
            raise HTTPException(404, 'SZ asset not found')
        await self.repo.delete(asset=asset)

    async def update(self, asset_id: int, payload: AssetUpdateAdm):
        asset = await self.repo.get_by_id(asset_id=asset_id)
        if asset is None:
            raise HTTPException(404, 'SZ asset not found')
        await self.repo.update(asset=asset, obj_in=payload)
        return asset
