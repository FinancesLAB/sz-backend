from sqlalchemy import Text, Integer, DateTime
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )