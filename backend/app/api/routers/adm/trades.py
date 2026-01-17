from fastapi import APIRouter, status, Depends
from app.schemas.trade import TradeCreate, TradeResponse, TradeUpdate
from app.services.trades import TradeService

from app.api.deps import get_trade_service

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.get("/{trade_id}")
async def get_trade(
    trade_id: int, service: TradeService = Depends(get_trade_service)
) -> TradeResponse:
    return await service.get_trade_by_trade_id(trade_id=trade_id)


@router.get("/")
async def get_trades(
    service: TradeService = Depends(get_trade_service),
) -> list[TradeResponse]:
    return await service.get_all_trades()


@router.post("/")
async def create_trade(
    payload: TradeCreate, service: TradeService = Depends(get_trade_service)
) -> TradeResponse:
    return await service.create(obj_in=payload)


@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade(
    trade_id: int, service: TradeService = Depends(get_trade_service)
):
    await service.delete_trade(trade_id=trade_id)
    return


@router.patch("/{trade_id}")
async def update(
    trade_id: int,
    payload: TradeUpdate,
    service: TradeService = Depends(get_trade_service),
):
    return await service.update(trade_id=trade_id, payload=payload)
