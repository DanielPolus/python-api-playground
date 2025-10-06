from fastapi import Depends, HTTPException, status, Query, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from typing import Optional, List
from app.db import get_db
from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate, AuthorOut

router = APIRouter(prefix="/authors",  tags=["authors"])

@router.post("/", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def post_author(payload: AuthorCreate, db: Session = Depends(get_db)):
    obj = Author(name=payload.name, bio=payload.bio)
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Author with this name already exists")

@router.get("/", response_model=List[AuthorOut], status_code=status.HTTP_200_OK)
def get_authors(
    q: Optional[str] = Query(None, min_length=2, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Author)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Author.name.like(like), Author.bio.like(like)))
    items = query.order_by(Author.id.desc()).offset(skip).limit(limit).all()
    return items

@router.get("/{author_id}", response_model=AuthorOut, status_code=status.HTTP_200_OK)
def get_author(author_id: int, db: Session = Depends(get_db)):
    obj = db.get(Author, author_id)
    if not obj:
        raise HTTPException(404, "Author not found")
    return obj

@router.patch("/{author_id}", response_model=AuthorOut, status_code=status.HTTP_200_OK)
def patch_author(author_id: int, payload: AuthorUpdate, db: Session = Depends(get_db)):
    author = db.query(Author).get(author_id)
    if not author:
        raise HTTPException(404, "Author not found")

    if payload.name is not None:
        author.name = payload.name
    if payload.bio is not None:
        author.bio = payload.bio

    try:
        db.commit()
        db.refresh(author)
        return author
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Author with this name already exists")

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).get(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
