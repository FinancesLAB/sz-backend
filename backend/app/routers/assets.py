# TODO: make endpoints ко всем хуйням описанным в айпаде (юри норм сделать тоже по ресту)
from fastapi import status
from fastapi import APIRouter
from app.core.database import SessionDep
from app.services.assets import AssetService
from app.schemas.asset import AssetSchema
router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("/")
async def get_assets(session: SessionDep):
    return await AssetService.get_all(session=session)

@router.get("/by-ticker/{ticker}")
async def get_asset_by_ticker(session: SessionDep, ticker: str):
    return await AssetService.get_by_ticker(session=session, ticker=ticker)

@router.get("/{asset_id}")
async def get_asset_by_id(session: SessionDep, asset_id: int):
    return await AssetService.get_by_id(session=session, asset_id=asset_id)

@router.post("/")
async def create_asset(session: SessionDep, asset_schema: AssetSchema):
    return await AssetService.create(session=session, asset_schema=asset_schema)

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session: SessionDep, asset_id: int):
    await AssetService.delete(session=session, asset_id=asset_id)
    return



# get by ticker