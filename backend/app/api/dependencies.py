from app.contracts.repos import PortfolioRepo, TradeRepo
from app.core.config import settings
from app.core.database import get_session
from app.services.analytics import AnalyticsService
from app.services.assets import AssetService
from app.services.auth import AuthService
from app.services.portfolios import PortfolioService
from app.services.trades import TradeService
from app.services.users import UserService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from shared.repositories.portfolio import PortfolioRepository
from shared.repositories.trade import TradeRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def get_portfolio_repo(session: AsyncSession = Depends(get_session)) -> PortfolioRepo:
    return PortfolioRepository(session=session)


async def get_portfolio_service(
    repo: PortfolioRepo = Depends(get_portfolio_repo),
) -> PortfolioService:
    return PortfolioService(repo=repo)


async def get_trade_repo(session: AsyncSession = Depends(get_session)) -> TradeRepo:
    return TradeRepository(session=session)


async def get_trade_service(repo: TradeRepo = Depends(get_trade_repo)) -> TradeService:
    return TradeService(repo=repo)


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session=session)


def get_asset_service(session: AsyncSession = Depends(get_session)) -> AssetService:
    return AssetService(session=session)


def get_analytics_service(
    session: AsyncSession = Depends(get_session),
) -> AnalyticsService:
    return AnalyticsService(session=session)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session=session)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get('type') != 'access':  # чтобы точно на рефреше не получили ничего
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type'
            )

        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    except JWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from err

    user = await service.get_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
