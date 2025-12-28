from fastapi import Depends, status
from fastapi import APIRouter
from app.api.deps import get_analytics_service
from app.services.analytics import AnalyticsService
from app.schemas.analytics import PortfolioShapshotResponse, SectorDistributionResponse, PortfolioDynamicsResponse
from app.api.deps import get_asset_service, get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/{portfolio_id}/shapshot") # допилить чтобы аналитика давала (или в ручке) список снэпшотов по всем портфолио
async def get_portfolio_shapshot_for_user(portfolio_id: int, current_user=Depends(get_current_user), service: AnalyticsService=Depends(get_analytics_service)) -> PortfolioShapshotResponse:
    return await service.portfolio_snapshot_for_user(portfolio_id=portfolio_id, user_id=current_user.id)

@router.get("/{portfolio_id}/sectors")
async def get_portfolio_sectors_distribution_for_user(portfolio_id: int, current_user=Depends(get_current_user), service: AnalyticsService=Depends(get_analytics_service))-> SectorDistributionResponse:
    return await service.sector_distribution_for_user(portfolio_id=portfolio_id, user_id=current_user.id)

@router.get("/{portfolio_id}/dynamics")
async def get_portfolio_dynamics_for_user(portfolio_id: int, current_user=Depends(get_current_user), service: AnalyticsService=Depends(get_analytics_service)) -> PortfolioDynamicsResponse:
    return await service.portfolio_dynamics_for_24h_for_user(portfolio_id=portfolio_id, user_id=current_user.id)