from datetime import datetime

from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column


class Trade(Base):
    __tablename__ = 'trades'

    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey('portfolios.id', ondelete='CASCADE'))
    asset_id: Mapped[int] = mapped_column(ForeignKey('assets.id'))
    direction: Mapped[str] = mapped_column(Text)  # buy/sell
    quantity: Mapped[float] = mapped_column(Numeric, nullable=False)
    price: Mapped[float] = mapped_column(Numeric, nullable=False)
    trade_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
