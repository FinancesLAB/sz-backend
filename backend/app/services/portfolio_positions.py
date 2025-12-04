from shared.repositories.portfolio_position import PortfolioPositionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.portfolio_position import PortfolioPositionUpdate, PortfolioPositionCreate

class PortfolioPositionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PortfolioPositionRepository(session=session)

    async def get_all(self):
        return await self.repo.get_all()
    
    async def get_by_id(self, portfolio_position_id: int):
        portfolio_position = await self.repo.get_by_id(
            portflio_position_id=portfolio_position_id
        )
        if portfolio_position is None:
            raise HTTPException(404, "SZ portfolio position not found")
        return portfolio_position
    
    async def get_by_portfolio_id(self, portfolio_id: int):
        portfolio_positions = await self.repo.get_by_portfolio_id(portfolio_id=portfolio_id)
        if not portfolio_positions:
            raise HTTPException(404, "SZ portfolio position not found")
        return portfolio_positions
    
    async def create(self, obj_in: PortfolioPositionCreate):
        return await self.repo.create(obj_in=obj_in)
    
    async def update(self, portfolio_position_id: int, payload: PortfolioPositionCreate):
        portfolio_position = await self.repo.get_by_id(portflio_position_id=portfolio_position_id)
        if portfolio_position is None: raise HTTPException(404, "SZ portfolio position not found")
        await self.repo.update(portfolio_position=portfolio_position, obj_in=payload)
        return portfolio_position
    
    async def delete(self, portfolio_position_id: int):
        portfolio_position = await self.repo.get_by_id(portflio_position_id=portfolio_position_id)
        if portfolio_position is None: raise HTTPException(404, "SZ portfolio position not found")
        await self.repo.delete(portfolio_position=portfolio_position)
