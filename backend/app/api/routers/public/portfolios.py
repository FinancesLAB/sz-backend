from app.api.dependencies import get_current_user, get_portfolio_service
from app.infrastructure.redis.deps import get_cache
from app.infrastructure.redis.redis_cache import RedisCache
from app.schemas.portfolio import (
    PortfolioCreatePublic,
    PortfolioResponseAdm,
    PortfolioUpdatePublic,
)
from app.services.portfolios import PortfolioService
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix='/portfolios', tags=['Portfolios'])


@router.get(
    '/',
    response_model=list[PortfolioResponseAdm],
    summary='Список всех портфелей пользователя.',
)  # todo
async def get_portfolios(
    current_user=Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
) -> list[PortfolioResponseAdm]:
    return await service.get_user_portfolios(user_id=current_user.id)


@router.get(
    '/{portfolio_id}',
    response_model=PortfolioResponseAdm,
    summary='Портфель по id.',
)
async def get_by_portfolio_id(
    portfolio_id: int,
    current_user=Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
    cache: RedisCache = Depends(get_cache),
) -> PortfolioResponseAdm:
    key = f'user:{current_user.id}:portfolio:{portfolio_id}:v1'

    cached = await cache.get_json(key)
    if cached is not None:
        return PortfolioResponseAdm.model_validate(cached)

    result = await service.get_portfolio_for_user(
        portfolio_id=portfolio_id, user_id=current_user.id
    )
    dto = PortfolioResponseAdm.model_validate(result, from_attributes=True)
    await cache.set_json(key, dto.model_dump(mode='json'), ttl=30)
    return dto


@router.delete(
    '/{portfolio_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить портфель по id.',
)
async def delete_by_id(
    portfolio_id: int,
    current_user=Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
):
    await service.delete_portfolio_for_user(portfolio_id=portfolio_id, user_id=current_user.id)
    return None


@router.post(
    '/',
    response_model=PortfolioResponseAdm,
    summary='Создать пустой портфель.',
)  # todo
async def create_portfolio_for_user(
    payload: PortfolioCreatePublic,
    current_user=Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioResponseAdm:
    return await service.create_portfolio_for_user(payload=payload, user_id=current_user.id)


@router.patch(
    '/{portfolio_id}',
    response_model=PortfolioResponseAdm,
    summary='Обновить информацию о портфеле.',
)
async def update_portfolio_for_user(
    portfolio_id: int,
    payload: PortfolioUpdatePublic,
    current_user=Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioResponseAdm:
    return await service.update_for_user(
        portfolio_id=portfolio_id, user_id=current_user.id, payload=payload
    )
