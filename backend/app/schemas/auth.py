from pydantic import BaseModel

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