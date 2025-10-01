from fastapi import FastAPI, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from typing import Optional, List
from db import Base, engine, get_db
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoOut

app = FastAPI(title="Todo API (SQLite + SQLAlchemy)")
Base.metadata.create_all(bind=engine)

NEXT_ID = 1
TODOS: List[dict] = []

def _find_todo_indes(todo_id: int) -> int:
    for i, t in enumerate(TODOS):
        if t["id"] == todo_id:
            return i
    return -1

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}

@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/todos", response_model=List[TodoOut])
def list_todos(
        q: Optional[str] = Query(None, min_length=1, max_length=200),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
):
    items = TODOS.copy()

    if q:
        needle = q.lower()
        items = [
            t for t in items
            if needle in t["title"].lower()
            or (t.get("description") or "").lower().find(needle) != -1
        ]

    items = sorted(items, key=lambda t: t["id"], reverse=True)
    return items[skip: skip + limit]

@app.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int):
    for t in TODOS:
        if t["id"] == todo_id:
            return t
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos-post", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def post_todo(payload: TodoCreate):
    global NEXT_ID
    todo = {
        "id": NEXT_ID,
        "title": payload.title,
        "description": payload.description,
        "done": payload.done,
        "created_at": payload.created_at
    }
    TODOS.append(todo)
    NEXT_ID += 1
    return todo

@app.patch("/todos/{todo_id}", response_model=TodoOut)
def patch_todo(todo_id: int, payload: TodoUpdate):
    idx = _find_todo_indes(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")

    data = payload.model_dump(exclude_unset=True)

    TODOS[idx].update(data)
    return TODOS[idx]

@app.put("/todos/{todo_id}", response_model=TodoOut)
def put_todo(todo_id: int, payload: TodoUpdate):
    idx = _find_todo_indes(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")

    preserved = {
        "id": TODOS[idx]["id"],
        "created_at": TODOS[idx]["created_at"],
    }

    TODOS[idx] = {
        **preserved,
        "title": payload.title,
        "description": payload.description,
        "done": payload.done
    }
    return TODOS[idx]

@app.delete("/todos/{todo_id}", response_model=TodoOut)
def delete_todo(todo_id: int):
    idx = _find_todo_indes(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    TODOS.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)