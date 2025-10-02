from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Integer, Numeric, ForeignKey
from db import Base
from decimal import Decimal
from datetime import datetime
from typing import Optional

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True, unique=True, nullable=False)

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    spent_at: Mapped[datetime] = mapped_column(DateTime, index=True, server_default=func.now())
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
