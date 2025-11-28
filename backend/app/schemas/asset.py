from pydantic import BaseModel, Field
from datetime import datetime

class AssetBase(BaseModel):
    ticker: str
    full_name: str
    type: str

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    ticker: str | None = None
    full_name: str | None = None
    type: str | None = None
    sector: str | None = None

class AssetResponse(AssetBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        