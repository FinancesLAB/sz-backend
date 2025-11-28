from shared.repositories.portfolio_position import PortfolioPositionRepository

from fastapi import HTTPException

class PortfolioPositionService:
    @staticmethod
    async def get_all(session):
        return await PortfolioPositionRepository.get_all(session=session)
    
    @staticmethod
    async def get_by_id(session, portfolio_position_id: int):
        portfolio_position = await PortfolioPositionRepository.get_by_id(
            session=session,
            portflio_position_id=portfolio_position_id
        )
        if portfolio_position is None:
            raise HTTPException(404, "SZ portfolio position not found")
        return portfolio_position
    
    @staticmethod
    async def create(session, portfolio_position_schema): # там аккуратно сам постгрес настроен что чекает зависимости и наличие айдишников
        return await PortfolioPositionRepository.create(
            session=session,
            portfolio_id=portfolio_position_schema.portfolio_id,
            asset_id=portfolio_position_schema.asset_id,
            quantity=portfolio_position_schema.quantity,
            avg_price=portfolio_position_schema.avg_price
        )
    
    @staticmethod
    async def delete(session, portfolio_position_id: int):
        portfolio_position = await PortfolioPositionRepository.get_by_id(
            session=session, 
            portflio_position_id=portfolio_position_id
            )
        if portfolio_position is None:
            raise HTTPException(404, "SZ portfolio position not found")
        
        await PortfolioPositionRepository.delete(session=session, portfolio_position=portfolio_position)