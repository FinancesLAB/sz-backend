from sqlalchemy import select
from shared.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj_in: UserCreate):
        obj=User(**obj_in.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def get_all(self):
        query = select(User)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
        
    async def update(self, user: User, obj_in: UserUpdate):
        update_data=obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete(self, user: User):
        await self.session.delete(user)
        await self.session.commit()

    
    
    
