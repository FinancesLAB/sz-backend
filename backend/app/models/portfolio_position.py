
from sqlalchemy import ForeignKey, DateTime, Numeric, UniqueConstraint
from backend.app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"
    __table_args__ = (UniqueConstraint("portfolio_id", "asset_id", name="uix_portfolio_asset"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE")
    )
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    quantity: Mapped[float] = mapped_column(Numeric, nullable=False)
    avg_price: Mapped[float] = mapped_column(Numeric, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
