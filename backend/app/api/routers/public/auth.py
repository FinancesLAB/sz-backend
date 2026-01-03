from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from passlib.context import CryptContext
from app.api.deps import get_user_service, get_current_user
from app.services.users import UserService
from app.schemas.user import UserCreateAdm
from app.schemas.auth import Token, RegisterIn
from app.schemas.user import UserResponsePublic
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
import hashlib

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterIn, service: UserService = Depends(get_user_service)) -> UserResponsePublic:
    existing = await service.get_by_email(payload.email)
    if existing: raise HTTPException(status_code=409, detail="User already exists")

    user = await service.create(UserCreateAdm(name=payload.name, email=payload.email, hashed_password=hash_password(payload.password)))
   
    return UserResponsePublic(name=user.name, email=user.email)

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

# class RefreshSessionIn(BaseModel):
#     user_id
#     jti
#     token_hash
#     expires_at
    
@router.post("/login", response_model=Token)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], service: UserService = Depends(get_user_service), db: AsyncSession = Depends(get_session)):
    user = await service.get_by_email(form.username)
    
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    access_token = create_access_token(user_id=user.id)

    refresh_jti = uuid4().hex
    refresh_token = create_refresh_token(user_id=user.id,jti=refresh_jti)
    refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    session = RefreshSession(
        user_id=user.id,
        jti=refresh_jti,
        token_hash=hash_token(refresh_token),
        expires_at=refresh_expires_at,
    )

    db.add(session)
    await db.commit()

    return Token(access_token=access_token, refresh_token=refresh_token)
    
from jose import JWTError, jwt
from app.schemas.auth import RefreshIn, LogoutIn

@router.post("/refresh", response_model=Token)
async def refresh(payload: RefreshIn, db: AsyncSession = Depends(get_session)):
    try:
        decoded = jwt.decode(
            payload.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=401)

        user_id = decoded.get("sub")
        jti = decoded.get("jti")

        if not user_id or not jti:
            raise HTTPException(status_code=401)

    except JWTError:
        raise HTTPException(status_code=401)

    result = await db.execute(select(RefreshSession).where(RefreshSession.jti == jti))
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=401)

    if session.revoked_at is not None:
        raise HTTPException(status_code=401)

    if session.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=401)

    if session.token_hash != hash_token(payload.refresh_token):
        raise HTTPException(status_code=401)

    session.revoked_at = datetime.now(timezone.utc)

    new_jti = uuid4().hex

    new_refresh_token = create_refresh_token(user_id=int(user_id), jti=new_jti)

    new_refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    new_session = RefreshSession(
        user_id=int(user_id),
        jti=new_jti,
        token_hash=hash_token(new_refresh_token),
        expires_at=new_refresh_expires_at,
        created_at=datetime.now(timezone.utc),
    )

    session.replaced_by_jti = new_jti

    db.add(new_session)
    await db.commit()

    access_token = create_access_token(user_id=int(user_id))

    return Token(access_token=access_token, refresh_token=new_refresh_token)
    

@router.post("/logout", status_code=204)
async def logout(payload: LogoutIn, db: AsyncSession = Depends(get_session)):
    try:
        decoded = jwt.decode(payload.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        jti = decoded.get("jti")
    except JWTError:
        return

    await db.execute(
        update(RefreshSession)
        .where(RefreshSession.jti == jti)
        .values(revoked_at=datetime.now(timezone.utc))
    )
    await db.commit()