from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import UserService
from app.services.trades import TradeService
from fastapi import Depends
from app.core.database import get_session

def get_user_service(
        session: AsyncSession = Depends(get_session)
) -> UserService:
    return UserService(session=session)

async def get_trades_session(
        session: AsyncSession = Depends(get_session)
) -> TradeService:
    return TradeService(session=session)
