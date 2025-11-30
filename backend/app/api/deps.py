from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import UserService
from app.services.portfolio_positions import PortfolioPositionService
from app.services.assets import AssetService
from app.services.trades import TradeService
from app.services.portfolios import PortfolioService
from app.services.analytics import AnalyticsService
from fastapi import Depends
from app.core.database import get_session

def get_user_service(
        session: AsyncSession = Depends(get_session)
) -> UserService:
    return UserService(session=session)

def get_porfolio_service(session: AsyncSession = Depends(get_session)) -> PortfolioService:
    return PortfolioService(session=session)

def get_trade_service(
        session: AsyncSession = Depends(get_session)
) -> TradeService:
    return TradeService(session=session)

def get_porfolio_position_service(
        session: AsyncSession=Depends(get_session)
) -> PortfolioPositionService:
    return PortfolioPositionService(session=session)

def get_asset_service(
        session: AsyncSession=Depends(get_session)
) -> AssetService:
    return AssetService(session=session)

def get_analytics_service(
        session: AsyncSession=Depends(get_session)
) -> AnalyticsService:
    return AnalyticsService(session=session)