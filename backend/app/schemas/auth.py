from pydantic import BaseModel, ConfigDict
from pydantic.types import AwareDatetime


class APIModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class Token(APIModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshIn(APIModel):
    refresh_token: str


class RegisterIn(APIModel):
    name: str
    email: str
    password: str


class LogoutIn(APIModel):
    refresh_token: str


class RefreshSessionCreate(APIModel):
    user_id: int
    jti: str
    token_hash: str
    expires_at: AwareDatetime
