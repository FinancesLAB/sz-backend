from pydantic import BaseModel, Field
from pydantic.types import AwareDatetime


class AssetFields(BaseModel):
    ticker: str
    full_name: str
    type: str
    sector: str


class AssetResponsePublic(AssetFields):
    id: int


class AssetResponseAdm(AssetFields):
    id: int
    created_at: AwareDatetime


class AssetCreateAdm(AssetFields):
    pass


class AssetUpdateAdm(AssetFields):
    ticker: str | None = None
    full_name: str | None = None
    type: str | None = None
    sector: str | None = None
