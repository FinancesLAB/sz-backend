from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class TopPosition(BaseModel):
    asset_id: int =Field(..., description="asset ID")
    ticker: str =Field(..., description="asset ticker, for example: GAZP")
    full_name: str=Field(..., description="full name of asset")
    quantity: int=Field(..., description="quantity of asset")
    avg_buy_price: float=Field(..., description="average buy price of asset")
    current_price: float=Field(..., description="current price of asset")
    current_value: float=Field(..., description="current value of position (quantity * current_price)")
    profit: float= Field(..., description="absolute profit of asset")
    profit_percent: float=Field(..., description="profit of asset in percents")
    weight_percent: float=Field(..., description="weight of asset in portfolio in percents")


class PortfolioShapshotResponse(BaseModel): # rename
    portfolio_id: int=Field(..., description="portfolio ID")
    name: str=Field(..., description="portfolio name")
    total_value: float=Field(..., description="current value of portfolio")
    total_profit: float=Field(..., description="current profit of portfolio")
    total_profit_percent: float=Field(..., description="current porfit of portfolio in percents")
    invested_value: float=Field(..., description="value invested in portfolio initially")
    currency: str=Field(..., description="currency of portfolio, for example: RUB")
    positions_count: int=Field(..., description="number of unique assets in portfolio")
    top_positions: List[TopPosition]=Field(..., description="top 3 positions in portfolio by value part in portfolio")


class SectorPositions(BaseModel):
    sector: str
    current_value: float
    weight_percent: float

class SectorDistributionResponse(BaseModel):
    portfolio_id : int
    total_value: float
    sectors: List[SectorPositions]