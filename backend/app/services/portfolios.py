from app.repositories.portfolios import PortfolioRepository

from fastapi import HTTPException

class PortfolioService:
    @staticmethod
    async def get_all(session):
        return await PortfolioRepository.get_all(session=session)
    
    @staticmethod
    async def get_by_id(session, portfolio_id: int):
        portfolio = await PortfolioRepository.get_by_id(session=session, portfolio_id=portfolio_id)
        if portfolio is None:
            raise HTTPException(404, "SZ user not found")
        return portfolio
    


# сделать получение всей инфы по всем портфелям (с дждоинами) юзера либо по конкретному портфелю (чисто айди портфеля)