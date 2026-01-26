from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class TradeDTO:
    asset_id: int
    direction: str
    quantity: Decimal
    price: Decimal

    @classmethod
    def from_orm(cls, trade):
        return cls(
            asset_id=trade.asset_id,
            direction=trade.direction,
            quantity=trade.quantity,
            price=trade.price,
        )


@dataclass
class Lot:
    qty: Decimal
    price: Decimal


@dataclass
class PortfolioPositionPrepared:
    asset_id: int
    asset_market_price: Decimal
    ticker: str
    name: str
    sector: str
    lots: deque[Lot] = field(default_factory=deque)

    @property
    def mid_price(self):
        total = Decimal(0)
        qty = Decimal(0)
        for lot in self.lots:
            total += lot.qty * lot.price
            qty += lot.qty
        return total / qty

    @property
    def quantity(self):
        qty = Decimal(0)
        for lot in self.lots:
            qty += lot.qty
        return qty

    @property
    def cost_basis(self):
        cost_basis = Decimal(0)
        for lot in self.lots:
            cost_basis += lot.qty * lot.price
        return cost_basis

    @property
    def unrealized_pnl(self):
        absolute_profit = self.market_price - self.mid_price * self.quantity
        return absolute_profit

    @property
    def unrealized_return_pct(self):
        return (self.unrealized_pnl / self.cost_basis) * 100

    @property
    def market_price(self):
        return self.quantity * self.asset_market_price


@dataclass
class SectorPosition:
    sector: str
    market_value: Decimal


@dataclass
class DynamicsPosition:
    asset_id: int
    quantity: Decimal


@dataclass
class TimeSerie:
    timestamp: datetime
    price: Decimal
