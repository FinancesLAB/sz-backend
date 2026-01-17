from pydantic import BaseModel, Field
from pydantic.types import AwareDatetime


class UserFields(BaseModel):
    name: str
    email: str


class UserCreatePublic(UserFields):
    pass


class UserCreateAdm(UserFields):
    hashed_password: str | None = None


class UserUpdatePublic(UserFields):
    name: str | None = None
    email: str | None = None


class UserUpdateAdm(UserFields):
    name: str | None = None
    email: str | None = None
    hashed_password: str | None = None


class UserResponsePublic(UserFields):
    pass


class UserResponseAdm(UserFields):
    id: int
    hashed_password: str
    created_at: AwareDatetime
