from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    done: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow())

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    done: Optional[bool] = None

class TodoOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool
    created_at: datetime

    class Config:
        from_attributes = True