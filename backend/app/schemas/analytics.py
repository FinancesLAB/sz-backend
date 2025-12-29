from datetime import datetime
from pydantic import BaseModel, Field

class TopPosition(BaseModel):
    asset_id: int =Field(..., description="asset ID in position (inner)")
    ticker: str =Field(..., description="asset ticker, for example: GAZP")
    full_name: str=Field(..., description="full name of asset in position")
    quantity: int=Field(..., description="quantity of asset in position")
    avg_buy_price: float=Field(..., description="average buy price of asset in position")
    asset_market_price: float=Field(..., description="current market price of 1 asset in position")
    market_value: float=Field(..., description="current market price of all assets in position")
    unrealized_pnl: float= Field(..., description="unrealized PNL of portfolio position")
    unrealized_return_pct: float=Field(..., description=" profit of asset in percents")
    weight_pct: float=Field(..., description="weight of asset in portfolio in percents")


class PortfolioShapshotResponse(BaseModel):
    portfolio_id: int=Field(..., description="portfolio ID")
    name: str=Field(..., description="portfolio name")
    market_value: float=Field(..., description="total current value of portfolio")
    unrealized_pnl: float=Field(..., description="unrealized PNL of portfolio")
    unrealized_return_pct: float=Field(..., description="unreleazed return of portfolio")
    cost_basis: float=Field(..., description="value invested in portfolio initially")
    currency: str=Field(..., description="currency of portfolio, for example: RUB")
    positions_count: int=Field(..., description="number of unique assets in portfolio")
    top_positions: list[TopPosition]=Field(..., description="top 3 positions in portfolio by value part in portfolio")

    @classmethod
    def empty(cls, portfolio):
        return cls(
            portfolio_id = portfolio.id,
            name = portfolio.name,
            market_value = 0,
            unrealized_pnl = 0,
            unrealized_return_pct = 0,
            cost_basis = 0,
            currency = portfolio.currency,
            positions_count = 0,
            top_positions = []
        )



class SectorDistributionPosition(BaseModel):
    sector: str=Field(..., description="sector name, for example \"retail\"")
    market_value: float=Field(..., description="current value of portfolio assets from stated sector")
    weight_percent: float=Field(..., description="current percent value of portfolio assets from stated sector to whole current portfolio value")

class SectorDistributionResponse(BaseModel):
    portfolio_id : int=Field(..., description="portfolio ID")
    name: str=Field(..., description="portfolio name")
    market_value: float=Field(..., description="total market value of portfolio")
    currency: str=Field(..., description="currency of portfolio, for example: RUB")
    sectors: list[SectorDistributionPosition]

    @classmethod
    def empty(cls, portfolio):
        return cls(
            portfolio_id=portfolio.id,
            name=portfolio.name,
            market_value=0,
            currency=portfolio.currency,
            sectors=[]
        )



class PortfolioPrice(BaseModel):
    timestamp: datetime=Field(..., description="Timestamp in iso8601")
    total_value: float=Field(..., description="total value of portfolio at selectet timestamp")

class PortfolioDynamicsResponse(BaseModel):
    portfolio_id : int=Field(..., description="portfolio ID")
    name: str=Field(..., description="portfolio name")
    data: list[PortfolioPrice]

    @classmethod
    def empty(cls, portfolio):
        return cls(
            portfolio_id = portfolio.id,
            name = portfolio.name,
            data = []
        )