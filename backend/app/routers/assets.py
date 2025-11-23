# TODO: make endpoints ко всем хуйням описанным в айпаде (юри норм сделать тоже по ресту)
from fastapi import status
from fastapi import APIRouter
from app.core.database import SessionDep
from app.services.assets import AssetsService
from app.schemas.asset import AssetSchema
router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("/")
async def get_assets(session: SessionDep):
    return await AssetsService.get_all(session=session)

@router.get("/{asset_id}")
async def get_asset(session: SessionDep, asset_id: int):
    return await AssetsService.get_one(session=session, asset_id=asset_id)

@router.post("/")
async def create_asset(session: SessionDep, asset_schema: AssetSchema):
    return await AssetsService.create(session=session, asset_schema=asset_schema)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session: SessionDep, asset_id: int):
    await AssetsService.delete(session=session, asset_id=asset_id)
    return

# get by ticker