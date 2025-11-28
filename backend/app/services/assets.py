from backend.app.repositories.assets import AssetRepository

from fastapi import HTTPException

class AssetService:
    @staticmethod
    async def get_all(session):
        return await AssetRepository.get_all(session=session)
    
    @staticmethod
    async def get_by_id(session, asset_id: int):
        asset = await AssetRepository.get_by_id(session=session, asset_id=asset_id)
        if asset is None:
            raise HTTPException(404, "SZ asset not found")
        return asset
    
    @staticmethod
    async def get_by_ticker(session, ticker: str):
        asset = await AssetRepository.get_by_ticker(session=session, ticker=ticker)
        if asset is None:
            raise HTTPException(404, "SZ asset not found")
        return asset
    
    @staticmethod
    async def create(session, asset_schema):
        return await AssetRepository.create(session=session, 
                                             ticker=asset_schema.ticker, 
                                             full_name=asset_schema.full_name,
                                             type=asset_schema.type
                                             )

    @staticmethod
    async def delete(session, asset_id: int):
        asset = await AssetRepository.get_by_id(session=session, asset_id=asset_id)
        if asset is None:
            raise HTTPException(404, "SZ asset not found")
        
        await AssetRepository.delete(session=session, asset=asset)
    
    @staticmethod 
    async def update(session, asset_id: int, data: dict):
        asset = await AssetRepository.get_by_id(session=session, asset_id=asset_id)
        if asset is None:
            raise HTTPException(404, "SZ asset not found")
        
        await AssetRepository.update(session=session, asset=asset, data=data)
