from app.api.dependencies import get_analytics_service, get_current_user
from app.schemas.analytics import (
    PortfolioDynamicsResponse,
    PortfolioSnapshotResponse,
    SectorDistributionResponse,
)
from app.services.analytics import AnalyticsService
from fastapi import APIRouter, Depends

router = APIRouter(prefix='/analytics', tags=['Analytics'])


@router.get(
    '/{portfolio_id}/snapshot',
    response_model=PortfolioSnapshotResponse,
    summary='Актуальная сводка информации + 3 топ позиции по портфелю.',
)  # допилить чтобы аналитика давала (или в ручке) список снэпшотов по всем портфолио
async def get_portfolio_snapshot_for_user(
    portfolio_id: int,
    current_user=Depends(get_current_user),
    service: AnalyticsService = Depends(get_analytics_service),
) -> PortfolioSnapshotResponse:
    return await service.portfolio_snapshot_for_user(
        portfolio_id=portfolio_id, user_id=current_user.id
    )


@router.get(
    '/{portfolio_id}/sectors',
    response_model=SectorDistributionResponse,
    summary="Распределение портфеля по секторам."
)
async def get_portfolio_sectors_distribution_for_user(
    portfolio_id: int,
    current_user=Depends(get_current_user),
    service: AnalyticsService = Depends(get_analytics_service),
) -> SectorDistributionResponse:
    return await service.sector_distribution_for_user(
        portfolio_id=portfolio_id, user_id=current_user.id
    )


@router.get(
    '/{portfolio_id}/dynamics/24h',
    response_model=PortfolioDynamicsResponse,
    summary="Динамика портфеля за последние 24 часа"
)
async def get_portfolio_dynamics_for_user(
    portfolio_id: int,
    current_user=Depends(get_current_user),
    service: AnalyticsService = Depends(get_analytics_service),
) -> PortfolioDynamicsResponse:
    return await service.portfolio_dynamics_for_24h_for_user(
        portfolio_id=portfolio_id, user_id=current_user.id
    )
