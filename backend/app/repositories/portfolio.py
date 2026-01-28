from app.schemas.portfolio import (
    PortfolioCreateAdm,
    PortfolioCreatePublic,
    PortfolioUpdateAdm,
)
from app.models import Portfolio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PortfolioRepositoryPostgres:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: PortfolioCreateAdm):
        obj = Portfolio(**payload.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_all(self):
        query = select(Portfolio)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, portfolio_id: int):
        query = select(Portfolio).where(Portfolio.id == portfolio_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, portfolio: Portfolio, payload: PortfolioUpdateAdm):
        update_data = payload.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(portfolio, field, value)
        await self.session.commit()
        await self.session.refresh(portfolio)
        return portfolio

    async def delete(self, portfolio: Portfolio):
        await self.session.delete(portfolio)
        await self.session.commit()

    async def get_by_user_id(self, user_id: int):
        query = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await self.session.execute(query)
        portfolios = result.scalars().all()
        return portfolios

    async def create_for_user(self, payload: PortfolioCreatePublic, user_id: int):
        obj = Portfolio(
            user_id=user_id,
            name=payload.name,
            currency=payload.currency,
        )
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
