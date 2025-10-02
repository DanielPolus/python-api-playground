from pydantic import field_validator, constr, ConfigDict, BaseModel, Field, condecimal
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ExpenseCreate(BaseModel):
    amount: condecimal(gt=0, max_digits=12, decimal_places=2) = Field(...)
    currency: constr(pattern=r'^[A-Z]{3}$') = Field(...)
    description: Optional[str] = Field(None, max_length=200)
    spent_at: datetime = Field(default_factory=datetime.utcnow)
    category_id: int = Field(..., gt=0)

    @field_validator("currency", mode="before")   # <— ВАЖНО: mode="before"
    @classmethod
    def normalize_currency(cls, v: str) -> str:
        v = str(v).strip().upper()
        if len(v) != 3 or not v.isalpha():
            raise ValueError("currency must be 3 letters, e.g. 'USD'")
        return v


class ExpenseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    amount: Decimal
    currency: str
    description: Optional[str] = None
    spent_at: datetime
    category_id: int

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        if not v:
            raise ValueError("name cannot be empty")
        v = v.strip().title()
        return v

class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str