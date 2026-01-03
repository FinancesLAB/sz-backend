from shared.models.refresh_sessions import RefreshSession
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.auth import RefreshSessionCreate
from shared.repositories.refresh_session import RefreshSessionRepository
from shared.repositories.user import UserRepository
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.schemas.auth import Token, RegisterIn
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from app.core.config import settings
import hashlib

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
  
  
from fastapi import Depends
from app.schemas.auth import RefreshIn
from jose import JWTError, jwt
from sqlalchemy import select, update
from app.schemas.auth import RefreshIn, LogoutIn
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserResponsePublic, UserCreateAdm

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
        refresh_token = create_refresh_token(user_id=user.id,jti=refresh_jti)
        refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        session = RefreshSessionCreate(
            user_id=user.id,
            jti=refresh_jti,
            token_hash=hash_token(refresh_token),
            expires_at=refresh_expires_at
        )
        await self.rs_repo.create(obj_in=session)
        
        return Token(access_token=access_token, refresh_token=refresh_token)
      
      async def refresh(self, payload: RefreshIn):
          try:
              decoded = jwt.decode(payload.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
              if decoded.get("type") != "refresh": raise HTTPException(status_code=401)
              user_id = decoded.get("sub")
              jti = decoded.get("jti")
              if not user_id or not jti: raise HTTPException(status_code=401)
          except JWTError: raise HTTPException(status_code=401)
          
          result = await self.session.execute(select(RefreshSession).where(RefreshSession.jti == jti))
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

          self.session.add(new_session)
          await self.session.commit()

          access_token = create_access_token(user_id=int(user_id))

          return Token(access_token=access_token, refresh_token=new_refresh_token)
        
      async def logout(self, payload: LogoutIn):
        try:
          decoded = jwt.decode(payload.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
          jti = decoded.get("jti")
        except JWTError:
            return

        await self.session.execute(
            update(RefreshSession)
            .where(RefreshSession.jti == jti)
            .values(revoked_at=datetime.now(timezone.utc))
        )
        await self.session.commit()
        
      async def register(self, payload: RegisterIn):
        existing = await self.user_repo.get_by_email(payload.email)
        if existing: raise HTTPException(status_code=409, detail="User already exists")

        user = await self.user_repo.create(UserCreateAdm(name=payload.name, email=payload.email, hashed_password=hash_password(payload.password)))
      
        return UserResponsePublic(name=user.name, email=user.email)        