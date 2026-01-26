from datetime import datetime
from decimal import Decimal

from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column


class AssetPrice(Base):
    __tablename__ = 'asset_prices'

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey('assets.id', ondelete='CASCADE'), nullable=False
    )
    price: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    currency: Mapped[str] = mapped_column(Text, default='RUB', nullable=False)
    source: Mapped[str] = mapped_column(Text, default='moex', nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
