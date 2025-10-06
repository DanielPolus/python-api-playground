from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, Integer, ForeignKey, Table, Column
from app.db import Base
from datetime import datetime
from typing import Optional, List

book_genres = Table(
    "book_genres",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    bio: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    books: Mapped[List["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    books: Mapped[List["Book"]] = relationship(
        secondary=book_genres,
        back_populates="genres"
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id"))
    published_year: Mapped[Optional[int]] = mapped_column(Integer)
    pages: Mapped[Optional[int]] = mapped_column(Integer)
    isbn: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)

    author: Mapped[List["Author"]] = relationship(back_populates="books")
    genres: Mapped[List["Genre"]] = relationship(
        secondary=book_genres,
        back_populates="books"
    )
