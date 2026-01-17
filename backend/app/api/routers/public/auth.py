from fastapi import APIRouter, Depends, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import get_auth_service
from app.schemas.auth import RefreshIn, LogoutIn, Token, RegisterIn
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterIn, service: AuthService = Depends(get_auth_service)
):
    return await service.register(payload=payload)


@router.post("/login", response_model=Token)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(username=form.username, password=form.password)


@router.post("/refresh", response_model=Token)
async def refresh(payload: RefreshIn, service: AuthService = Depends(get_auth_service)):
    return await service.refresh(payload)


@router.post("/logout", status_code=204)
async def logout(payload: LogoutIn, service: AuthService = Depends(get_auth_service)):
    return await service.logout(payload=payload)
