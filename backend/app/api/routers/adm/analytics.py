from fastapi import Depends, status
from fastapi import APIRouter
from app.api.deps import get_analytics_service
from app.services.analytics import AnalyticsService
from app.schemas.analytics import (
    PortfolioSnapshotResponse,
    SectorDistributionResponse,
    PortfolioDynamicsResponse,
)
from app.api.deps import get_asset_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/{portfolio_id}/shapshot")
async def get_portfolio_shapshot(
    portfolio_id: int, service: AnalyticsService = Depends(get_analytics_service)
) -> PortfolioSnapshotResponse:
    return await service.portfolio_snapshot(portfolio_id=portfolio_id)


@router.get("/{portfolio_id}/sectors")
async def get_portfolio_sectors_distribution(
    portfolio_id: int, service: AnalyticsService = Depends(get_analytics_service)
) -> SectorDistributionResponse:
    return await service.sector_distribution(portfolio_id=portfolio_id)


@router.get("/{portfolio_id}/dynamics")
async def get_portfolio_dynamics(
    portfolio_id: int, service: AnalyticsService = Depends(get_analytics_service)
) -> PortfolioDynamicsResponse:
    return await service.portfolio_dynamics_for_24h(portfolio_id)
