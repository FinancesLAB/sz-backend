from sqlalchemy import select
from app.models.user import UsersModel

class UsersRepository:
    @staticmethod
    async def get_one(user_id: int, session):
        query = select(UsersModel).where(UsersModel.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    @staticmethod
    async def create(session, name: str, age: int):
        new_user = UsersModel(
            name=name, 
            age=age
            )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user) # достать + айдишник от бд
        return new_user
    
    @staticmethod
    async def delete(session, user: UsersModel):
        await session.delete(user)
        await session.commit()
    
    @staticmethod
    async def get_all(session):
        query = select(UsersModel)
        result = await session.execute(query)
        return result.scalars().all()
