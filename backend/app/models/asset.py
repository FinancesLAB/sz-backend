from datetime import datetime

from app.infrastructure.db.database import Base
from sqlalchemy import DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column


class Asset(Base):
    __tablename__ = 'assets'

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    sector: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
