from sqlalchemy import select
from app.models.portfolio import Portfolio

class PortfolioRepository:
    @staticmethod
    async def get_all(session):
        query = select(Portfolio)
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(session, portfolio_id: int):
        query = select(Portfolio).where(Portfolio.id == portfolio_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    

