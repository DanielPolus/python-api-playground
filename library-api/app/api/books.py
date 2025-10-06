from fastapi import Depends, HTTPException, status, Query, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from app.db import get_db
from app.models import Book, Author, Genre
from sqlalchemy import or_
from app.schemas import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/books", tags=["books"])

def to_book_out(book: Book) -> BookOut:
    return BookOut(
        id=book.id,
        title=book.title,
        author_id=book.author_id,
        published_year=book.published_year,
        pages=book.pages,
        isbn=book.isbn,
        genre_ids=[g.id for g in book.genres],
    )

@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def post_book(payload: BookCreate, db: Session = Depends(get_db)):
    author = db.get(Author, payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    genres = []
    if payload.genre_ids:
        genres = db.query(Genre).filter(Genre.id.in_(payload.genre_ids)).all()
        missing = set(payload.genre_ids) - {g.id for g in genres}
        if missing:
            raise HTTPException(status_code=404, detail=f"Genre not found: {sorted(missing)}")

    book = Book(
        title=payload.title,
        author_id=payload.author_id,
        published_year=payload.published_year,
        pages=payload.pages,
        isbn=payload.isbn,
    )
    book.genres = genres

    db.add(book)
    try:
        db.commit()
        db.refresh(book)
        return to_book_out(book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Book violates unique constraint (likely ISBN)")

@router.get("/", response_model=List[BookOut], status_code=status.HTTP_200_OK)
def get_books(
    q: Optional[str] = Query(None, min_length=2, max_length=200),
    author_id: Optional[int] = Query(None, ge=1),
    genre_id: Optional[int] = Query(None, ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Book)

    if q:
        like = f"%{q}%"
        query = query.filter(or_(Book.title.like(like), Book.isbn.like(like)))

    if author_id is not None:
        query = query.filter(Book.author_id == author_id)

    if genre_id is not None:
        query = query.join(Book.genres).filter(Genre.id == genre_id)

    items = query.order_by(Book.id.desc()).offset(skip).limit(limit).all()
    return [to_book_out(b) for b in items]

@router.get("/{book_id}", response_model=BookOut, status_code=status.HTTP_200_OK)
def get_book(book_id: int, db: Session = Depends(get_db)):
    obj = db.get(Book, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    return to_book_out(obj)


@router.patch("/{book_id}", response_model=BookOut, status_code=status.HTTP_200_OK)
def patch_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # author
    if payload.author_id is not None:
        author = db.get(Author, payload.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        book.author_id = payload.author_id

    # genres (полная замена, если поле передано)
    if payload.genre_ids is not None:
        genres = db.query(Genre).filter(Genre.id.in_(payload.genre_ids)).all()
        missing = set(payload.genre_ids) - {g.id for g in genres}
        if missing:
            raise HTTPException(status_code=404, detail=f"Genre not found: {sorted(missing)}")
        book.genres = genres

    # остальные поля
    if payload.title is not None:
        book.title = payload.title
    if payload.published_year is not None:
        book.published_year = payload.published_year
    if payload.pages is not None:
        book.pages = payload.pages
    if payload.isbn is not None:
        book.isbn = payload.isbn

    try:
        db.commit()
        db.refresh(book)
        return to_book_out(book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Book violates unique constraint (likely ISBN)")

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    obj = db.get(Book, book_id)
    if not obj:
        raise HTTPException(404, "Book not found")

    db.delete(obj)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

