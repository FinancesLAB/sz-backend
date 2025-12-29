from fastapi import Depends, status
from fastapi import APIRouter
from app.services.assets import AssetService
from app.schemas.asset import AssetResponsePublic
from app.api.deps import get_asset_service

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("/{asset_id}")
async def get_asset_by_id(asset_id: int, service: AssetService=Depends(get_asset_service)) -> AssetResponsePublic:
    return await service.get_by_id(asset_id=asset_id)

@router.get("/by-ticker/{ticker}")
async def get_asset_by_ticker(ticker: str, service: AssetService=Depends(get_asset_service)) -> AssetResponsePublic:
    return await service.get_by_ticker(ticker=ticker)

@router.get("/")
async def get_assets(service: AssetService=Depends(get_asset_service)) -> list[AssetResponsePublic]:
    return await service.get_all()
