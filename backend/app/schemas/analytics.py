from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import AwareDatetime, NonNegativeInt, PositiveInt


class APIModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Currency(str, Enum):
    RUB = "RUB"
    USD = "USD"


Money = Annotated[
    float,
    Field(description="Money value", ge=0),
]

Percent = Annotated[
    float,
    Field(description="Percent value", ge=-100, le=10_000),
]


class TopPosition(APIModel):
    asset_id: PositiveInt = Field(..., description="Asset ID in position")
    ticker: str = Field(..., description="Asset ticker, for example: GAZP")
    full_name: str = Field(..., description="Full name of asset in position")
    quantity: NonNegativeInt = Field(..., description="Quantity of asset in position")
    avg_buy_price: Money = Field(..., description="Average buy price of asset in position")
    asset_market_price: Money = Field(
        ..., description="Current market price of 1 asset in position"
    )
    market_value: Money = Field(..., description="Current market price of all assets in position")
    unrealized_pnl: float = Field(..., description="Unrealized PNL of portfolio position")
    unrealized_return_pct: Percent = Field(..., description="Profit of asset in percents")
    weight_pct: Percent = Field(..., description="Weight of asset in portfolio in percents")


class PortfolioSnapshotResponse(APIModel):
    portfolio_id: PositiveInt = Field(..., description="Portfolio ID")
    name: str = Field(..., description="Portfolio name")
    market_value: Money = Field(..., description="Total current value of portfolio")
    unrealized_pnl: float = Field(..., description="Unrealized PNL of portfolio")
    unrealized_return_pct: Percent = Field(..., description="Unrelized return of portfolio")
    cost_basis: Money = Field(..., description="Value invested in portfolio initially")
    currency: Currency = Field(..., description="Currency of portfolio, for example: RUB")
    positions_count: NonNegativeInt = Field(..., description="Number of unique assets in portfolio")
    top_positions: list[TopPosition] = Field(
        default_factory=list,
        description="Top 3 positions in portfolio by value part in portfolio",
        max_length=3,
    )

    @classmethod
    def empty(cls, portfolio):
        return cls(
            portfolio_id=portfolio.id,
            name=portfolio.name,
            market_value=0,
            unrealized_pnl=0,
            unrealized_return_pct=0,
            cost_basis=0,
            currency=portfolio.currency,
            positions_count=0,
            top_positions=[],
        )


class SectorDistributionPosition(APIModel):
    sector: str = Field(..., description='Sector name, for example "retail"')
    market_value: Money = Field(
        ..., description="Current value of portfolio assets from stated sector"
    )
    weight_percent: Percent = Field(
        ...,
        description=(
        "Current percent value of portfolio assets from stated sector "
        "to whole current portfolio value"
    ),
    )


class SectorDistributionResponse(APIModel):
    portfolio_id: PositiveInt = Field(..., description="Portfolio ID")
    name: str = Field(..., description="Portfolio name")
    market_value: Money = Field(..., description="Total market value of portfolio")
    currency: Currency = Field(..., description="Currency of portfolio, for example: RUB")
    sectors: list[SectorDistributionPosition] = Field(
        default_factory=list, description="Portfolio grouped and distributed by sectors"
    )

    @classmethod
    def empty(cls, portfolio):
        return cls(
            portfolio_id=portfolio.id,
            name=portfolio.name,
            market_value=0,
            currency=portfolio.currency,
            sectors=[],
        )


class PortfolioPrice(APIModel):
    timestamp: AwareDatetime = Field(..., description="Timestamp in iso8601")
    total_value: Money = Field(..., description="Total value of portfolio at selected timestamp")


class PortfolioDynamicsResponse(APIModel):
    portfolio_id: PositiveInt = Field(..., description="Portfolio ID")
    name: str = Field(..., description="Portfolio name")
    data: list[PortfolioPrice] = Field(
        default_factory=list, description="List of relations timestamp to price"
    )

    @classmethod
    def empty(cls, portfolio):
        return cls(portfolio_id=portfolio.id, name=portfolio.name, data=[])
