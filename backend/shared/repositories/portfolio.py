from sqlalchemy import select
from shared.models.portfolio import Portfolio

class PortfolioRepository:
    @staticmethod
    async def get_by_id(session, portfolio_id: int):
        query = select(Portfolio).where(Portfolio.id == portfolio_id)
        result = await session.execute(query)
        portfolio = result.scalar_one_or_none()
        return portfolio
    
    @staticmethod
    async def get_all(session):
        query = select(Portfolio)
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def create(session, user_id: int, name: str):
        new_portfolio = Portfolio(
            user_id=user_id,
            name=name
        )
        session.add(new_portfolio)
        await session.commit()
        await session.refresh(new_portfolio)
        return new_portfolio
    
    @staticmethod
    async def delete(session, portfolio: Portfolio):
        await session.delete(portfolio)
        await session.commit()

    @staticmethod
    async def get_by_user_id(session, user_id: int):
        query = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await session.execute(query)
        portfolios = result.scalars().all()
        return portfolios
    

