from shared.repositories.portfolio import PortfolioRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.portfolio import PortfolioCreatePublic, PortfolioUpdatePublic


class PortfolioService:
    def __init__(self, session):
        self.session = session
        self.repo = PortfolioRepository(session=session)

    async def get_all_portfolios(self):
        return await self.repo.get_all()

    async def get_portfolio_by_portfolio_id(self, portfolio_id: int):
        portfolio = await self.repo.get_by_id(portfolio_id=portfolio_id)
        if portfolio is None:
            raise HTTPException(404, "SZ portfolio not found")
        return portfolio

    async def create_portfolio(self, obj_in: PortfolioCreatePublic):
        return await self.repo.create(obj_in=obj_in)

    async def delete_portfolio_by_portfolio_id(self, portfolio_id: int):
        portfolio = await self.repo.get_by_id(portfolio_id=portfolio_id)
        if portfolio is None:
            raise HTTPException(404, "SZ portfolio not found")

        await self.repo.delete(portfolio=portfolio)

    async def update(self, portfolio_id: int, payload: PortfolioUpdatePublic):
        portfolio = await self.repo.get_by_id(portfolio_id=portfolio_id)
        if portfolio is None:
            raise HTTPException(404, "SZ portfolio not found")
        await self.repo.update(portfolio=portfolio, obj_in=payload)
        return portfolio

    async def get_user_portfolios(self, user_id: int):
        return await self.repo.get_by_user_id(user_id=user_id)

    # for user
    async def get_portfolio_for_user(self, portfolio_id: int, user_id: int):
        portfolio = await self.repo.get_by_id(portfolio_id=portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        if portfolio.user_id != user_id:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        return portfolio

    async def create_portfolio_for_user(
        self, user_id: int, payload: PortfolioCreatePublic
    ):
        return await self.repo.create_for_user(payload=payload, user_id=user_id)

    async def delete_portfolio_for_user(self, portfolio_id: int, user_id: int):
        portfolio = await self.repo.get_by_id(portfolio_id=portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        if portfolio.user_id != user_id:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        await self.repo.delete(portfolio=portfolio)

    async def update_for_user(
        self, portfolio_id: int, user_id: int, payload: PortfolioUpdatePublic
    ):
        portfolio = await self.repo.get_by_id(portfolio_id=portfolio_id)
        if not portfolio:
            raise HTTPException(404, "SZ portfolio not found")
        if portfolio.user_id != user_id:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        await self.repo.update(portfolio=portfolio, payload=payload)
        return portfolio
