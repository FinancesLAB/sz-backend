from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import hashlib
from jose import JWTError
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(user_id: int) -> str:
    expirates_at = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id), 
        "type": "access",
        "exp": expirates_at,
        "iat": datetime.now(timezone.utc)
        }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: int, jti: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "type": "refresh",
        "exp": expires_at,
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def hash_of_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def get_jti_from_token(token: str):
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return decoded.get("jti")

class InvalidRefreshToken(Exception):
    pass


def decode_refresh_token(token: str) -> tuple[int, str]:
    try:
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise InvalidRefreshToken()

    if decoded.get("type") != "refresh":
        raise InvalidRefreshToken()

    user_id = decoded.get("sub")
    jti = decoded.get("jti")

    if not user_id or not jti:
        raise InvalidRefreshToken()

    return int(user_id), jti