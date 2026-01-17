from fastapi import APIRouter, status, Depends
from app.schemas.user import UserResponsePublic, UserUpdatePublic
from app.api.deps import get_user_service, get_current_user
from app.services.users import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponsePublic)
async def get_user(
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserResponsePublic:
    return await service.get_by_id(user_id=current_user.id)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    await service.delete_user(user_id=current_user.id)
    return None


@router.patch("/me", response_model=UserResponsePublic)
async def update(
    payload: UserUpdatePublic,
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserResponsePublic:
    return await service.update(user_id=current_user.id, payload=payload)
