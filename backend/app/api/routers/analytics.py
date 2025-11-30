from fastapi import Depends, status
from fastapi import APIRouter
from app.api.deps import get_analytics_service
from app.services.analytics import AnalyticsService
from app.schemas.analytics import PortfolioShapshotResponse
from app.api.deps import get_asset_service
router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/{portfolio_id}", response_model=PortfolioShapshotResponse)
async def get_analytics(portfolio_id: int, service: AnalyticsService=Depends(get_analytics_service)):
    return await service.portfolio_snapshot(portfolio_id=portfolio_id)
