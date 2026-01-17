from fastapi import APIRouter, status, Depends
from app.schemas.user import UserCreateAdm, UserResponseAdm, UserUpdateAdm
from app.api.deps import get_user_service
from app.services.users import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", summary="Get detailed user info by user_id")
async def get_user(
    user_id: int, service: UserService = Depends(get_user_service)
) -> UserResponseAdm:
    return await service.get_by_id(user_id=user_id)


@router.get("/", summary="Get all users detailed info")
async def get_users(
    service: UserService = Depends(get_user_service),
) -> list[UserResponseAdm]:
    return await service.get_all()


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create user")
async def create_user(
    payload: UserCreateAdm, service: UserService = Depends(get_user_service)
) -> UserResponseAdm:
    return await service.create(obj_in=payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user by user_id",
)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    await service.delete_user(user_id=user_id)
    return None


@router.patch("/{user_id}", summary="Update user bu user_id")
async def update(
    user_id: int,
    payload: UserUpdateAdm,
    service: UserService = Depends(get_user_service),
) -> UserResponseAdm:
    return await service.update(user_id=user_id, payload=payload)
