from shared.repositories.user import UserRepository

from fastapi import HTTPException

class UserService:
    @staticmethod
    async def get_all(session):
        return await UserRepository.get_all(session=session)
    
    @staticmethod
    async def get_by_user_id(session, user_id: int):
        user = await UserRepository.get_by_id(session=session, user_id=user_id)
        if user is None:
            raise HTTPException(404, "SZ user not found")
        return user

    @staticmethod
    async def create_user(session, user_schema):
        return await UserRepository.create(
            session=session,
            name=user_schema.name,
            age=user_schema.age
            )

    @staticmethod
    async def delete_user(session, user_id: int):
        user = await UserRepository.get_by_id(session=session, user_id=user_id)
        if user is None:
            raise HTTPException(404, "SZ user not found")
        
        await UserRepository.delete(session=session, user=user)