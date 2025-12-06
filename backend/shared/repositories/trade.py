from sqlalchemy import select
from shared.models.trade import Trade
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.trade import TradeCreate, TradeUpdate

class TradeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj_in: TradeCreate):
        obj=Trade(**obj_in.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def get_all(self):
        query = select(Trade)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, trade_id: int):
        query = select(Trade).where(Trade.id == trade_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def update(self, trade: Trade, obj_in: TradeUpdate):
        update_data=obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(trade, field, value)
        await self.session.commit()
        await self.session.refresh(trade)
        return trade
    
    async def delete(self, trade: Trade):
        await self.session.delete(trade)
        await self.session.commit()

    async def get_trades_by_portfolio_id(self, portfolio_id: int):
        query = select(Trade).where(Trade.portfolio_id == portfolio_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    

    
