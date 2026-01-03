from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from passlib.context import CryptContext
from app.api.deps import get_user_service, get_current_user, get_refresh_session_service
from app.services.users import UserService
from app.schemas.auth import Token, RegisterIn
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from jose import JWTError, jwt
from app.schemas.auth import RefreshIn, LogoutIn
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from shared.models.refresh_sessions import RefreshSession
from app.core.database import get_session
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.schemas.auth import RefreshSessionCreate
from app.services.auth import AuthService
from sqlalchemy import update

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterIn, service: AuthService = Depends(get_refresh_session_service)):
    return await service.register(payload=payload)

@router.post("/login", response_model=Token)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthService = Depends(get_refresh_session_service)):
    return await service.login(username=form.username, password=form.password)
 
@router.post("/refresh", response_model=Token)
async def refresh(payload: RefreshIn, service: AuthService = Depends(get_refresh_session_service)):
    return await service.refresh(payload)

@router.post("/logout", status_code=204)
async def logout(payload: LogoutIn, service: AuthService = Depends(get_refresh_session_service)):
    return await service.logout(payload=payload)