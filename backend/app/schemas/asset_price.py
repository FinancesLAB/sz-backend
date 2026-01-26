from decimal import Decimal

from pydantic import BaseModel
from pydantic.types import AwareDatetime


class AssetPriceBase(BaseModel):
    asset_id: int
    price: Decimal
    currency: str
    source: str


class AssetPriceCreate(AssetPriceBase):
    pass


class AssetPriceUpdate(AssetPriceBase):
    asset_id: int | None = None
    price: Decimal | None = None
    currency: str | None = None
    source: str | None = None


class AssetPriceResponse(AssetPriceBase):
    id: int
    timestamp: AwareDatetime

    class Config:
        from_attributes = True
