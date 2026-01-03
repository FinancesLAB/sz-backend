from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import UserService
from app.services.assets import AssetService
from app.services.trades import TradeService
from app.services.portfolios import PortfolioService
from app.services.analytics import AnalyticsService
from app.services.refresh_session import RefreshSessionService
from fastapi import Depends, HTTPException, status
from app.core.database import get_session
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError


def get_user_service(
        session: AsyncSession = Depends(get_session)
) -> UserService:
    return UserService(session=session)

def get_portfolio_service(session: AsyncSession = Depends(get_session)) -> PortfolioService:
    return PortfolioService(session=session)

def get_trade_service(
        session: AsyncSession = Depends(get_session)
) -> TradeService:
    return TradeService(session=session)

def get_asset_service(
        session: AsyncSession=Depends(get_session)
) -> AssetService:
    return AssetService(session=session)

def get_analytics_service(
        session: AsyncSession=Depends(get_session)
) -> AnalyticsService:
    return AnalyticsService(session=session)

def get_refresh_session_service(
    session: AsyncSession=Depends(get_session)
) -> RefreshSessionService:
    return RefreshSessionService(session=session)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), service: UserService = Depends(get_user_service)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type") != "access": # чтобы точно на рефреше не получили ничего
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await service.get_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user