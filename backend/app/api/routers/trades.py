from fastapi import APIRouter, status, Depends
from app.schemas.trade import TradeCreate, TradeResponse
from app.services.trades import TradeService
from app.api.deps import get_trades_session
router = APIRouter(prefix="/trades", tags=["Trades"])

@router.get("/{trade_id}", response_model=TradeResponse)
async def get_trade(trade_id: int, service: TradeService=Depends(get_trades_session)):
    return await service.get_trade_by_trade_id(trade_id=trade_id)

@router.get("/", response_model=list[TradeResponse])
async def get_trades(service: TradeService=Depends(get_trades_session)):
    return await service.get_all_trades()

@router.post("/", response_model=TradeResponse)
async def create_trade(trade_schema: TradeCreate, service: TradeService=Depends(get_trades_session)):
    return await service.create(trade_schema=trade_schema)

@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade(trade_id: int, service: TradeService=Depends(get_trades_session)):
    await service.delete_trade(trade_id=trade_id)
    return
    