from pydantic import BaseModel
from datetime import datetime
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshIn(BaseModel):
    refresh_token: str
    
class RegisterIn(BaseModel):
    name: str
    email: str
    password: str
    
class LogoutIn(BaseModel):
    refresh_token: str
    
class RefreshSessionCreate(BaseModel):
    user_id: int
    jti: str
    token_hash: str
    expires_at: datetime