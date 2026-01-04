from sqlalchemy import select, update
from shared.models.refresh_sessions import RefreshSession
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import RefreshSessionCreate
from datetime import datetime, timezone



class RefreshSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, obj_in: RefreshSessionCreate):
        obj = RefreshSession(**obj_in.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
        
    async def get_by_jti(self, jti: str):
        result = await self.session.execute(select(RefreshSession).where(RefreshSession.jti == jti))
        return result.scalar_one_or_none()
 
    async def set_revoke_by_jti(self, jti: str):
        await self.session.execute(
            update(RefreshSession).where(RefreshSession.jti == jti).values(revoked_at=datetime.now(timezone.utc))
        )
        await self.session.commit()