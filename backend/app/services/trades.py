from requests import session
from shared.repositories.trade import TradeRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

class TradeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TradeRepository(session=session)

    async def get_all_trades(self):
        return await self.repo.get_all()
    
    async def get_trade_by_trade_id(self, trade_id: int):
        trade = await self.repo.get_by_id(trade_id=trade_id)
        if trade is None:
            raise HTTPException(404, "SZ trade not found")
        return trade

    async def create(self, trade_schema):
        return await self.repo.create(
            portfolio_id=trade_schema.portfolio_id,
            asset_id=trade_schema.asset_id,
            direction=trade_schema.direction,
            quantity=trade_schema.quantity,
            price=trade_schema.price
            )

    async def delete_trade(self, trade_id: int):
        trade = await self.get_trade_by_trade_id(trade_id=trade_id)
        if trade is None:
            raise HTTPException(404, "SZ trade not found")
        
        await self.repo.delete(trade=trade)