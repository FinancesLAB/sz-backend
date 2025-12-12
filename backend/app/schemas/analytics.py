from datetime import datetime
from pydantic import BaseModel, Field
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


class PortfolioShapshotResponse(BaseModel):
    portfolio_id: int=Field(..., description="portfolio ID")
    name: str=Field(..., description="portfolio name")
    market_value: float=Field(..., description="total current value of portfolio")
    unrealized_pnl: float=Field(..., description="unrealized PNL of portfolio")
    unrealized_return_pct: float=Field(..., description="unreleazed return of portfolio")
    cost_basis: float=Field(..., description="value invested in portfolio initially")
    currency: str=Field(..., description="currency of portfolio, for example: RUB")
    positions_count: int=Field(..., description="number of unique assets in portfolio")
    top_positions: List[TopPosition]=Field(..., description="top 3 positions in portfolio by value part in portfolio")

    @classmethod
    def empty(cls, portfolio):
        return cls(
            portfolio_id = portfolio.id,
            name = portfolio.name,
            total_value = 0,
            total_profit = 0,
            total_profit_percent = 0,
            invested_value = 0,
            currency = portfolio.currency,
            positions_count = 0,
            top_positions = []
        )



class SectorPosition(BaseModel):
    sector: str=Field(..., description="sector name, for example \"retail\"")
    current_value: float=Field(..., description="current value of portfolio assets from stated sector")
    weight_percent: float=Field(..., description="current percent value of portfolio assets from stated sector to whole current portfolio value")

class SectorDistributionResponse(BaseModel):
    portfolio_id : int=Field(..., description="portfolio ID")
    name: str=Field(..., description="portfolio name")
    total_value: float=Field(..., description="total current value of portfolio")
    currency: str=Field(..., description="currency of portfolio, for example: RUB")
    sectors: List[SectorPosition]

    @classmethod
    def empty(cls, portfolio):
        return cls(
            portfolio_id = portfolio.id,
            name = portfolio.name,
            total_value = 0,
            currency = portfolio.currency,
            sectors = []
        )



class PortfolioPrice(BaseModel):
    timestamp: datetime=Field(..., description="Timestamp in iso8601")
    total_value: float=Field(..., description="total value of portfolio at selectet timestamp")

class PortfolioDynamicsResponse(BaseModel):
    portfolio_id : int=Field(..., description="portfolio ID")
    name: str=Field(..., description="portfolio name")
    data: List[PortfolioPrice]

    @classmethod
    def empty(cls, portfolio):
        return cls(
            portfolio_id = portfolio.id,
            name = portfolio.name,
            data = []
        )