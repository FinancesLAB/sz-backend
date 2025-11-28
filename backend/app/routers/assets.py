# TODO: make endpoints ко всем хуйням описанным в айпаде (юри норм сделать тоже по ресту)
from fastapi import status
from fastapi import APIRouter
from backend.app.core.database import SessionDep
from backend.app.services.assets import AssetService
from backend.app.schemas.asset import AssetCreate, AssetResponse, AssetUpdate
router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("/", response_model=list[AssetResponse])
async def get_assets(session: SessionDep):
    return await AssetService.get_all(session=session)

@router.get("/by-ticker/{ticker}", response_model=AssetResponse)
async def get_asset_by_ticker(session: SessionDep, ticker: str):
    return await AssetService.get_by_ticker(session=session, ticker=ticker)

@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset_by_id(session: SessionDep, asset_id: int):
    return await AssetService.get_by_id(session=session, asset_id=asset_id)

@router.post("/", response_model=AssetResponse)
async def create_asset(session: SessionDep, asset_schema: AssetCreate):
    return await AssetService.create(session=session, asset_schema=asset_schema)

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(session: SessionDep, asset_id: int):
    await AssetService.delete(session=session, asset_id=asset_id)
    return

@router.patch("/{asset_id}")
async def update_asset(session: SessionDep, asset_id: int, payload: AssetUpdate):
    updated = await AssetService.update(session=session, asset_id=asset_id, data=payload.dict(exclude_unset=True))
    await session.commit()
    return updated
## TODO : add sector column to other cruds