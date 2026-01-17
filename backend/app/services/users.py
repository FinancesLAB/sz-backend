from shared.repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.user import UserCreateAdm, UserUpdateAdm


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session=session)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, user_id: int):
        user = await self.repo.get_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(404, "SZ user not found")
        return user

    async def get_by_email(self, email: str):
        user = await self.repo.get_by_email(email=email)
        return user

    async def create(self, obj_in: UserCreateAdm):
        return await self.repo.create(obj_in=obj_in)

    async def delete_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(404, "SZ user not found")
        await self.repo.delete(user=user)

    async def update(self, user_id: int, payload: UserUpdateAdm):
        user = await self.repo.get_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(404, "SZ user not found")
        await self.repo.update(user=user, obj_in=payload)
        return user
