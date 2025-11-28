from sqlalchemy import select
from shared.models.trade import Trade

class TradeRepository:
    @staticmethod
    async def get_by_id(trade_id: int, session):
        query = select(Trade).where(Trade.id == trade_id)
        result = await session.execute(query)
        trade = result.scalar_one_or_none()
        return trade
    
    @staticmethod
    async def get_all(session):
        query = select(Trade)
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def create(session, portfolio_id: int, asset_id: int, direction: str, quantity: int, price: int):
        new_trade = Trade(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
            direction=direction,
            quantity=quantity,
            price=price
        )
        session.add(new_trade)
        await session.commit()
        await session.refresh(new_trade) # достать + айдишник от бд
        return new_trade
    
    @staticmethod
    async def delete(session, trade: Trade):
        await session.delete(trade)
        await session.commit()
    
    
