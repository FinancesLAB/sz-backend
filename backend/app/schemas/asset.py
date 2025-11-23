from pydantic import BaseModel, Field

class AssetSchema(BaseModel):
    ticker: str
    full_name: str
    type: str