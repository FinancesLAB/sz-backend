from sqlalchemy import select
from backend.app.models.portfolio_position import PortfolioPosition

class PortfolioPositionRepository:
    @staticmethod
    async def get_all(session):
        query = select(PortfolioPosition)
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(session, portflio_position_id: int):
        query = select(PortfolioPosition).where(PortfolioPosition.id == portflio_position_id)
        result = await session.execute(query)
        portflio_position = result.scalar_one_or_none()
        return portflio_position
    
    @staticmethod
    async def create(session, portfolio_id: int, asset_id: int, quantity: int, avg_price: int):
        new_portflio_position = PortfolioPosition(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
            quantity=quantity,
            avg_price=avg_price
        )
        session.add(new_portflio_position)
        await session.commit()
        await session.refresh(new_portflio_position)
        return new_portflio_position
    
    @staticmethod
    async def delete(session, portfolio_position: PortfolioPosition):
        await session.delete(portfolio_position)
        await session.commit()

    @staticmethod
    async def get_by_portfolio_id(session, portfolio_id):
        query = select(PortfolioPosition).where(PortfolioPosition.portfolio_id == portfolio_id)
        portfolio_positions = await session.execute(query)
        return portfolio_positions.scalars.all()
