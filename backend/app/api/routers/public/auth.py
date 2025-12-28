from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from passlib.context import CryptContext
from app.api.deps import get_user_service, get_current_user
from app.services.users import UserService
from app.schemas.user import UserCreate
from app.schemas.auth import Token, RegisterIn, UserPublic
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterIn, service: UserService = Depends(get_user_service)) -> UserPublic:
    existing = await service.get_by_email(payload.email)
    if existing: raise HTTPException(status_code=409, detail="User already exists")

    user = await service.create(UserCreate(name=payload.name, email=payload.email, hashed_password=hash_password(payload.password)))
   
    return UserPublic(id=user.id, name=user.name, email=user.email)

@router.post("/login")
async def login(form:  Annotated[OAuth2PasswordRequestForm, Depends()], service: UserService = Depends(get_user_service)) -> Token:
    user = await service.get_by_email(form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="access troubles")

    token = create_access_token(user_id=str(user.id))
    return Token(access_token=token)

@router.get("/me")
async def me(current_user=Depends(get_current_user)) -> UserPublic:
    return UserPublic(id=current_user.id, name=current_user.name, email=current_user.email)