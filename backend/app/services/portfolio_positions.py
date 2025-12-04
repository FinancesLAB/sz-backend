from shared.repositories.portfolio_position import PortfolioPositionRepository
from shared.repositories.asset import AssetRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.portfolio_position import PortfolioPositionUpdate, PortfolioPositionCreate, PrettyPortfolioPosition

class PortfolioPositionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.portfolio_position_repo = PortfolioPositionRepository(session=session)
        self.asset_repo = AssetRepository(session=session)

    async def get_all(self):
        return await self.portfolio_position_repo.get_all()
    
    async def get_by_id(self, portfolio_position_id: int):
        portfolio_position = await self.portfolio_position_repo.get_by_id(
            portflio_position_id=portfolio_position_id
        )
        if portfolio_position is None:
            raise HTTPException(404, "SZ portfolio position not found")
        return portfolio_position
    
    async def get_by_portfolio_id(self, portfolio_id: int):
        portfolio_positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id=portfolio_id)
        if not portfolio_positions:
            return []
        resp = list()
        for pos in portfolio_positions:
            asset = await self.asset_repo.get_by_id(pos.asset_id)
            resp.append(
                PrettyPortfolioPosition(
                    id=pos.id,
                    quantity=pos.quantity,
                    created_at=pos.created_at,
                    asset_id=pos.asset_id,
                    ticker=asset.ticker,
                    avg_price=pos.avg_price
                )
            )
        return resp
    
    async def create(self, obj_in: PortfolioPositionCreate):
        return await self.portfolio_position_repo.create(obj_in=obj_in)
    
    async def update(self, portfolio_position_id: int, payload: PortfolioPositionCreate):
        portfolio_position = await self.portfolio_position_repo.get_by_id(portflio_position_id=portfolio_position_id)
        if portfolio_position is None: raise HTTPException(404, "SZ portfolio position not found")
        await self.portfolio_position_repo.update(portfolio_position=portfolio_position, obj_in=payload)
        return portfolio_position
    
    async def delete(self, portfolio_position_id: int):
        portfolio_position = await self.portfolio_position_repo.get_by_id(portflio_position_id=portfolio_position_id)
        if portfolio_position is None: raise HTTPException(404, "SZ portfolio position not found")
        await self.portfolio_position_repo.delete(portfolio_position=portfolio_position)
