from enum import Enum
from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from pydantic.types import AwareDatetime

T = TypeVar('T')


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=200)
    offset: int = Field(ge=0)


class AssetType(str, Enum):
    stock = 'stock'
    bond = 'bond'
    fund = 'fund'


AssetTypeField = Annotated[AssetType, Field(description='Вид актива')]


class AssetSector(str, Enum):
    oil_gas = 'oil_gas'
    utilities = 'utilities'
    telecom = 'telecom'
    metals_mining = 'metals_mining'
    financials = 'financials'
    consumer = 'consumer'
    chemicals = 'chemicals'
    it = 'it'
    real_estate = 'real_estate'
    transport = 'transport'


AssetSectorField = Annotated[AssetSector, Field(description='Сектор, к которому относится акция')]

Ticker = Annotated[
    str,
    Field(
        min_length=1,
        max_length=12,
        pattern=r'^[A-Z0-9._-]+$',
        description='Тикер, уникальный индентификатор актива на бриже',
        examples=['SBER', 'GAZP', 'T'],
    ),
]

AssetFullName = Annotated[
    str,
    Field(
        min_length=1,
        max_length=200,
        description='Полное название актива',
        examples=['Газпром', 'Сбербанк ПАО'],
    ),
]


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class AssetFields(APIModel):
    ticker: Ticker
    full_name: AssetFullName
    type: AssetTypeField
    sector: AssetSectorField


class AssetResponsePublic(AssetFields):
    id: PositiveInt
    model_config = ConfigDict(
        from_attributes=True,
    )


class AssetResponseAdm(AssetFields):
    id: PositiveInt
    created_at: AwareDatetime


class AssetCreateAdm(AssetFields):
    pass


class AssetUpdateAdm(AssetFields):
    ticker: Ticker | None = None
    full_name: AssetFullName | None = None
    type: AssetTypeField | None = None
    sector: AssetSectorField | None = None
