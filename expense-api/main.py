from fastapi import FastAPI, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from typing import Optional, List
from db import Base, engine, get_db
from models import Expense, Category
from schemas import ExpenseCreate, ExpenseOut, CategoryCreate, CategoryOut

app = FastAPI(title="Expense Tracker API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def post_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    obj = Category(name=payload.name)
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category with this name already exists")

@app.get("/categories", response_model=List[CategoryOut])
def get_categories(
        q: Optional[str] = Query(None, min_length=1, max_length=200),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db),
):
    query = db.query(Category)
    if q:
        like = f"%{q}%"
        query = query.filter(Category.name.like(like))
    items = query.order_by(Category.id.desc()).offset(skip).limit(limit).all()
    return items

@app.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    obj = db.get(Category, category_id)
    if not obj:
        raise HTTPException(404, "Category not found")
    return obj

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    obj = db.get(Category, category_id)
    if not obj:
        raise HTTPException(404, "Category not found")
    if db.query(Expense).filter_by(category_id=category_id).count() > 0:
        raise HTTPException(409, "Category has related expenses")

    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#______________EXPENSES_______________#

@app.post("/expenses", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def post_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    if not db.get(Category,payload.category_id):
        raise HTTPException(422, "no such category id")

    obj = Expense(
        amount=payload.amount,
        currency=payload.currency,
        description=payload.description,
        spent_at=payload.spent_at,
        category_id=payload.category_id
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

@app.get("/expenses", response_model=List[ExpenseOut])
def get_expenses(
        q: Optional[str] = Query(None, min_length=1, max_length=200),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    query =db.query(Expense)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Expense.description.like(like),
                Expense.currency.like(like))
        )

    items = query.order_by(Expense.id.desc()).offset(skip).limit(limit).all()
    return items

@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    obj = db.get(Expense, expense_id)
    if not obj:
        raise HTTPException(404, "expense not found")
    return obj

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    obj = db.get(Expense, expense_id)
    if not obj:
        raise HTTPException(404, "expense not found")

    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)