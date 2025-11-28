from requests import session
from sqlalchemy import select
from shared.models.trade import Trade
from sqlalchemy.ext.asyncio import AsyncConnection

class TradeRepository:
    def __init__(self, session: AsyncConnection):
        self.session = session

    async def get_by_id(self, trade_id: int):
        query = select(Trade).where(Trade.id == trade_id)
        result = await self.session.execute(query)
        trade = result.scalar_one_or_none()
        return trade
    
    async def get_all(self):
        query = select(Trade)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create(self, portfolio_id: int, asset_id: int, direction: str, quantity: int, price: int):
        new_trade = Trade(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
            direction=direction,
            quantity=quantity,
            price=price
        )
        self.session.add(new_trade)
        await self.session.commit()
        await self.session.refresh(new_trade) # достать + айдишник от бд
        return new_trade
    
    async def delete(self, trade: Trade):
        await self.session.delete(trade)
        await self.session.commit()
    
    
