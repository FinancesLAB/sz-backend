from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.types import AwareDatetime, PositiveInt
from enum import Enum
from typing import Annotated

class APIModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        str_strip_whitespace=True,
    )
    
class Currency(str, Enum):
    RUB = "RUB"
    USD = "USD"

PortfolioName = Annotated[
    str,
    Field(
        description="Portfolio name",
        min_length=1,
        max_length=64,
        examples=["Main portfolio"],
    ),
]


class PortfolioFields(APIModel):
    name: PortfolioName
    currency: Currency = Field(..., description="Portfolio currency")

class PortfolioCreatePublic(PortfolioFields):
    pass

class PortfolioUpdatePublic(APIModel):
    name: PortfolioName | None = None
    currency: Currency | None = None
    
    @model_validator(mode="after")
    def at_least_one_field(self):
        if not self.model_dump(exclude_none=True):
            raise ValueError("At least one field must be provided")
        return self

class PortfolioCreateAdm(PortfolioFields):
    user_id: PositiveInt

class PortfolioUpdateAdm(APIModel):
    user_id: PositiveInt | None = None
    name: PortfolioName | None = None
    currency: Currency | None = None
    
    @model_validator(mode="after")
    def at_least_one_field(self):
        if not self.model_dump(exclude_none=True):
            raise ValueError("At least one field must be provided")
        return self

class PortfolioResponseAdm(PortfolioFields):
    id: PositiveInt
    user_id: PositiveInt
    created_at: AwareDatetime