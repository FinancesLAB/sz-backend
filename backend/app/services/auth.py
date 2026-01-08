from shared.models.refresh_sessions import RefreshSession
from fastapi import HTTPException
from app.schemas.auth import RefreshSessionCreate
from shared.repositories.refresh_session import RefreshSessionRepository
from shared.repositories.user import UserRepository
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_password,
    decode_refresh_token,
    InvalidRefreshToken,
    get_jti_from_token,
)
from app.schemas.auth import Token, RegisterIn
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from app.core.security import hash_of_refresh_token  
  
from fastapi import status
from app.schemas.auth import RefreshIn
from jose import JWTError, jwt
from app.schemas.auth import RefreshIn, LogoutIn
from app.schemas.user import UserResponsePublic, UserCreateAdm

# check db number of trans
class AuthService:
    def __init__(self, session):
        self.session = session
        self.rs_repo = RefreshSessionRepository(session=session)
        self.user_repo = UserRepository(session=session)
      
      
    async def login(self, username: str, password: str):
        user = await self.user_repo.get_by_email(username)
    
        if not user or not verify_password(password, user.hashed_password): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

        access_token = create_access_token(user_id=user.id)
        refresh_jti = uuid4().hex
        refresh_token = create_refresh_token(user_id=user.id, jti=refresh_jti)
        refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        await self.rs_repo.create(
            RefreshSessionCreate(
                user_id=user.id,
                jti=refresh_jti,
                token_hash=hash_of_refresh_token(refresh_token),
                expires_at=refresh_expires_at,
            )
        )

        return Token(access_token=access_token, refresh_token=refresh_token)
      
    async def refresh(self, payload: RefreshIn):
        try:
            user_id, jti = decode_refresh_token(token=payload.refresh_token)
        except InvalidRefreshToken: 
            raise HTTPException(status_code=401)
        
        rs = await self.rs_repo.get_by_jti(jti=jti)

        if (
            not rs 
            or rs.revoked_at is not None
            or rs.expires_at <= datetime.now(timezone.utc)
            or rs.token_hash != hash_of_refresh_token(payload.refresh_token)
        ): raise HTTPException(status_code=401)
        
        rs.revoked_at = datetime.now(timezone.utc)
        
        new_jti = uuid4().hex
        new_refresh_token = create_refresh_token(user_id=int(user_id), jti=new_jti)
        new_refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        new_rs = RefreshSession(
              user_id=int(user_id),
              jti=new_jti,
              token_hash=hash_of_refresh_token(new_refresh_token),
              expires_at=new_refresh_expires_at,
              created_at=datetime.now(timezone.utc),
          )

        rs.replaced_by_jti = new_jti

        self.session.add(new_rs)
        await self.session.commit()

        access_token = create_access_token(user_id=int(user_id))

        return Token(access_token=access_token, refresh_token=new_refresh_token)
        
    async def logout(self, payload: LogoutIn):
        try: 
            jti = get_jti_from_token(token=payload.refresh_token)
        except JWTError:
            return
        
        await self.rs_repo.set_revoke_by_jti(jti=jti)
        
    async def register(self, payload: RegisterIn):
        existing = await self.user_repo.get_by_email(payload.email)
        if existing: 
            raise HTTPException(status_code=409, detail="User already exists")
        user = await self.user_repo.create(
            UserCreateAdm(
                name=payload.name, 
                email=payload.email, 
                hashed_password=hash_password(payload.password),
                )
            )
        return UserResponsePublic(name=user.name, email=user.email)        