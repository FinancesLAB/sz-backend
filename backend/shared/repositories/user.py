from sqlalchemy import select
from shared.models.user import User

class UserRepository:
    @staticmethod
    async def get_by_id(user_id: int, session):
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    @staticmethod
    async def get_all(session):
        query = select(User)
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def create(session, name: str, age: int):
        new_user = User(
            name=name, 
            age=age
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user) # достать + айдишник от бд
        return new_user
    
    @staticmethod
    async def delete(session, user: User):
        await session.delete(user)
        await session.commit()
    
    
