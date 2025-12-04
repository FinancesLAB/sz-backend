from sqlalchemy import select, func
from shared.models.portfolio_position import PortfolioPosition
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.portfolio_position import PortfolioPositionUpdate, PortfolioPositionCreate

class PortfolioPositionRepository:
    def __init__(self, session: AsyncSession):
        self.session=session

    async def create(self, obj_in: PortfolioPositionCreate):
        obj=PortfolioPosition(**obj_in.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def get_all(self):
        query = select(PortfolioPosition)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, portflio_position_id: int):
        query = select(PortfolioPosition).where(PortfolioPosition.id == portflio_position_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_portfolio_id(self, portfolio_id: int):
        query = select(PortfolioPosition).where(PortfolioPosition.portfolio_id == portfolio_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(self, portfolio_position: PortfolioPosition, obj_in: PortfolioPositionUpdate):
        update_data=obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(portfolio_position, field, value)
        await self.session.commit()
        await self.session.refresh(portfolio_position)
        return portfolio_position

    async def delete(self, portfolio_position: PortfolioPosition):
        await self.session.delete(portfolio_position)
        await self.session.commit()

    async def get_by_portfolio_id(self, portfolio_id):
        query = select(PortfolioPosition).where(PortfolioPosition.portfolio_id == portfolio_id)
        portfolio_positions = await self.session.execute(query)
        return portfolio_positions.scalars().all()
    
    # gives asset_id from a concrete portfolio_position
    async def get_position_asset_id(self, portfolio_position_id: int):
        query = select(PortfolioPosition).where(PortfolioPosition.id == portfolio_position_id)
        position = await self.session.execute(query)
        return position.scalar_one().asset_id
    
    async def get_unique_assets_count_by_portfolio_id(self, portfolio_id: int):
        query = select(func.count()).select_from(PortfolioPosition).where(PortfolioPosition.portfolio_id == portfolio_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
