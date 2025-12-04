from pydantic import BaseModel
from datetime import datetime

# raw schemas for straigh repo answers
class PortfolioPositionBase(BaseModel):
    portfolio_id: int
    asset_id: int
    quantity: int
    avg_price: float

class PortfolioPositionCreate(PortfolioPositionBase):
    pass

class PortfolioPositionUpdate(PortfolioPositionBase):
    portfolio_id: int | None = None
    asset_id: int | None = None
    quantity: int | None = None
    avg_price: int | None = None

class PortfolioPositionResponse(PortfolioPositionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes=True



class PrettyPortfolioPosition(BaseModel):
    id: int
    quantity: int
    created_at: datetime
    asset_id: int
    ticker: str
    avg_price: float