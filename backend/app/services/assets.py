from app.repositories.assets import AssetsRepository

from fastapi import HTTPException

class AssetsService:
    @staticmethod
    async def get_all(session):
        return await AssetsRepository.get_all(session=session)
    
    @staticmethod
    async def get_one(session, asset_id: int):
        asset = await AssetsRepository.get_one(session=session, asset_id=asset_id)
        if asset is None:
            raise HTTPException(404, "SZ user not found")
        return asset

    @staticmethod
    async def create(session, asset_schema):
        return await AssetsRepository.create(session=session, 
                                             ticker=asset_schema.ticker, 
                                             full_name=asset_schema.full_name,
                                             type=asset_schema.type
                                             )

    @staticmethod
    async def delete(session, asset_id: int):
        asset = await AssetsRepository.get_one(session=session, asset_id=asset_id)
        if asset is None:
            raise HTTPException(404, "SZ user not found")
        
        await AssetsRepository.delete(session=session, asset=asset)
    