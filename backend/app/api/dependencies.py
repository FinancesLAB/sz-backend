from app.contracts.repos import PortfolioRepository, TradeRepoRepository, UserRepoRepository
from app.infrastructure.db.database import get_session
from app.repositories import (
    PortfolioRepositoryPostgres,
    TradeRepositoryPostgres,
    UserRepositoryPostgres,
)
from app.services.analytics import AnalyticsService
from app.services.assets import AssetService
from app.services.auth import AuthService
from app.services.portfolios import PortfolioService
from app.services.trades import TradeService
from app.services.users import UserService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_portfolio_repo(session: AsyncSession = Depends(get_session)) -> PortfolioRepository:
    return PortfolioRepositoryPostgres(session=session)


async def get_portfolio_service(
    repo: PortfolioRepository = Depends(get_portfolio_repo),
) -> PortfolioService:
    return PortfolioService(repo=repo)


async def get_trade_repo(session: AsyncSession = Depends(get_session)) -> TradeRepoRepository:
    return TradeRepositoryPostgres(session=session)


async def get_trade_service(repo: TradeRepoRepository = Depends(get_trade_repo)) -> TradeService:
    return TradeService(repo=repo)


async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepoRepository:
    return UserRepositoryPostgres(session=session)


async def get_user_service(repo: UserRepoRepository = Depends(get_user_repo)) -> UserService:
    return UserService(repo=repo)


def get_asset_service(session: AsyncSession = Depends(get_session)) -> AssetService:
    return AssetService(session=session)


def get_analytics_service(
    session: AsyncSession = Depends(get_session),
) -> AnalyticsService:
    return AnalyticsService(session=session)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session=session)


# get_access_token = OAuth2PasswordBearer(tokenUrl='/api/auth/login')
#
#
# async def get_current_user(
#     token: str = Depends(get_access_token),
#     service: UserService = Depends(get_user_service),
# ):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#
#         if payload.get('type') != 'access':  # чтобы точно на рефреше не получили ничего
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type'
#             )
#
#         user_id = payload.get('sub')
#         if not user_id:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#
#     except JWTError as err:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from err
#
#     user = await service.get_by_id(int(user_id))
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     return user
