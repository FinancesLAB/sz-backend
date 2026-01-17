from fastapi import Depends, status
from fastapi import APIRouter
from app.services.assets import AssetService
from app.schemas.asset import AssetCreateAdm, AssetResponseAdm, AssetUpdateAdm
from app.api.deps import get_asset_service

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/{asset_id}")
async def get_asset_by_id(
    asset_id: int, service: AssetService = Depends(get_asset_service)
) -> AssetResponseAdm:
    return await service.get_by_id(asset_id=asset_id)


@router.get("/by-ticker/{ticker}")
async def get_asset_by_ticker(
    ticker: str, service: AssetService = Depends(get_asset_service)
) -> AssetResponseAdm:
    return await service.get_by_ticker(ticker=ticker)


@router.get("/")
async def get_assets(
    service: AssetService = Depends(get_asset_service),
) -> list[AssetResponseAdm]:
    return await service.get_all()


@router.post("/")
async def create_asset(
    payload: AssetCreateAdm, service: AssetService = Depends(get_asset_service)
) -> AssetResponseAdm:
    return await service.create(payload)


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: int, service: AssetService = Depends(get_asset_service)
):
    await service.delete(asset_id=asset_id)
    return


@router.patch("/{asset_id}")
async def update_asset(
    asset_id: int,
    payload: AssetUpdateAdm,
    service: AssetService = Depends(get_asset_service),
) -> AssetResponseAdm:
    return await service.update(asset_id=asset_id, payload=payload)
