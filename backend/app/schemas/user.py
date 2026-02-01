from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.types import AwareDatetime


class APIModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid',
        str_strip_whitespace=True,
    )


class UserFields(APIModel):
    name: str
    email: EmailStr


class UserCreatePublic(UserFields):
    pass


class UserCreateAdm(UserFields):
    hashed_password: str | None = None


class UserUpdatePublic(UserFields):
    name: str | None = None
    email: EmailStr | None = None


class UserUpdateAdm(UserFields):
    name: str | None = None
    email: EmailStr | None = None
    hashed_password: str | None = None


class UserResponsePublic(UserFields):
    pass


class UserResponseAdm(UserFields):
    id: int
    hashed_password: str
    created_at: AwareDatetime
