from app.repositories.users import UsersRepository

from fastapi import HTTPException

class UsersService:
    @staticmethod
    async def get_one(session, user_id: int):
        user = await UsersRepository.get_one(session=session, user_id=user_id)
        if user is None:
            raise HTTPException(404, "SZ user not found")
        return user

    @staticmethod
    async def create(session, user_schema):
        return await UsersRepository.create(session=session, name=user_schema.name, age=user_schema.age)

    @staticmethod
    async def delete(session, user_id: int):
        user = await UsersRepository.get_one(session=session, user_id=user_id)
        if user is None:
            raise HTTPException(404, "SZ user not found")
        
        await UsersRepository.delete(session=session, user=user)
    
    @staticmethod
    async def get_all(session):
        return await UsersRepository.get_all(session=session)