from typing import Optional, List
from datetime import date

from pydantic import BaseModel, Field, field_validator, ConfigDict


# --------- Author ---------
def _validate_author_name(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    v = value.strip()
    if not v:
        raise ValueError("name cannot be empty")
    check = v.replace(" ", "").replace("-", "")
    if not check.isalpha():
        raise ValueError("name must contain only letters, spaces or hyphens")
    return v

class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    bio: Optional[str] = Field(None, max_length=1000)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v):
        return _validate_author_name(v)

class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    bio: Optional[str] = Field(None, max_length=1000)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v):
        return _validate_author_name(v)

class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    bio: Optional[str] = None


# --------- Genre ---------
class GenreCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)

class GenreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


# --------- Book ---------
CURRENT_YEAR = date.today().year

class BookCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author_id: int = Field(...)
    published_year: Optional[int] = Field(None, ge=1450, le=CURRENT_YEAR + 1)
    pages: Optional[int] = Field(None, ge=1)
    isbn: Optional[str] = Field(None)  # можно добавить regex позже
    genre_ids: List[int] = Field(default_factory=list)

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, v):
        if v is None:
            return v
        v = str(v).strip()
        if len(v) < 2:
            raise ValueError("title is too short")
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    author_id: Optional[int] = Field(None)
    published_year: Optional[int] = Field(None, ge=1450, le=CURRENT_YEAR + 1)
    pages: Optional[int] = Field(None, ge=1)
    isbn: Optional[str] = Field(None)
    genre_ids: Optional[List[int]] = Field(None)

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, v):
        if v is None:
            return v
        v = str(v).strip()
        if len(v) < 2:
            raise ValueError("title is too short")
        return v

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author_id: int
    published_year: Optional[int] = None
    pages: Optional[int] = None
    isbn: Optional[str] = None
    genre_ids: List[int] = []
