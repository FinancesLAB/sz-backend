from decimal import Decimal
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.types import AwareDatetime, PositiveInt


class APIModel(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        from_attributes=True,
        json_encoders={Decimal: lambda v: str(v)},
    )


class TradeDirection(str, Enum):
    buy = 'buy'
    sell = 'sell'


Money = Annotated[
    Decimal,
    Field(description='Money value', ge=0),
]


class TradeBase(APIModel):
    portfolio_id: PositiveInt = Field(..., description='Portfolio id')
    asset_id: PositiveInt = Field(..., description='Asset id')
    direction: TradeDirection = Field(..., description='Trade direction, buy or sell')
    quantity: Decimal = Field(..., description='Quantity of asset in this trade')
    price: Money = Field(..., description='Price of 1 asset at the moment of trade')
    trade_time: AwareDatetime = Field(
        ..., description='Datetime timestamp with timezone when the trade created'
    )


class TradeCreate(TradeBase):
    pass


class TradeUpdate(APIModel):
    portfolio_id: PositiveInt | None = Field(None, description='Portfolio id')
    asset_id: PositiveInt | None = Field(None, description='Asset id')
    direction: TradeDirection | None = Field(None, description='Trade direction, buy or sell')
    quantity: Decimal | None = Field(None, description='Quantity of asset in this trade')
    price: Money | None = Field(None, description='Price of 1 asset at the moment of trade')
    trade_time: AwareDatetime | None = Field(
        None, description='Datetime timestamp with timezone when the trade created'
    )

    @model_validator(mode='after')
    def at_least_one_field(self):
        if not self.model_dump(exclude_none=True):
            raise ValueError('At least one field must be provided')
        return self


class TradeResponse(TradeBase):
    id: PositiveInt = Field(..., description='Trade id')
    created_at: AwareDatetime = Field(
        ..., description='Datetime timestamp with timezone when the trade created in db'
    )
