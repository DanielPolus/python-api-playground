from fastapi import Depends, HTTPException, status, Query, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from app.db import get_db
from app.models import Genre
from app.schemas import GenreCreate, GenreUpdate, GenreOut

router = APIRouter(prefix="/genres", tags=["genres"])

@router.post("/", response_model=GenreOut, status_code=status.HTTP_201_CREATED)
def post_genre(payload: GenreCreate, db: Session = Depends(get_db)):
    obj = Genre(name=payload.name)
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Genre with this name already exists")

@router.get("/", response_model=List[GenreOut], status_code=status.HTTP_200_OK)
def get_genres(
    q: Optional[str] = Query(None, min_length=2, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Genre)
    if q:
        like = f"%{q}%"
        query = query.filter(Genre.name.like(like))
    items = query.order_by(Genre.id.desc()).offset(skip).limit(limit).all()
    return items

@router.get("/{genre_id}", response_model=GenreOut, status_code=status.HTTP_200_OK)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    obj = db.get(Genre, genre_id)
    if not obj:
        raise HTTPException(404, "Genre not found")
    return obj

@router.patch("/{genre_id}", response_model=GenreOut, status_code=status.HTTP_200_OK)
def patch_genre(genre_id: int, payload: GenreUpdate, db: Session = Depends(get_db)):
    obj = db.get(Genre, genre_id)
    if not obj:
        raise HTTPException(404, "Genre not found")

    if payload.name is not None:
        obj.name = payload.name

    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Genre with this name already exists")

@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    obj = db.get(Genre, genre_id)
    if not obj:
        raise HTTPException(404, "Genre not found")

    if obj.books:
        raise HTTPException(409, "Genre is in use by books")

    db.delete(obj)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
