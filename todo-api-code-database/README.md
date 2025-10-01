# Todo API (FastAPI + SQLite + SQLAlchemy)

A simple REST API for managing todos.  
Built with **FastAPI**, **SQLAlchemy ORM**, and **SQLite** as a lightweight database.

## Features
- Full CRUD operations (create, read, update, delete)
- Input validation with **Pydantic**
- Search & pagination in GET /todos
- Proper separation of models (SQLAlchemy) and schemas (Pydantic)
- Automatic docs at `/docs` (Swagger UI)
- Response codes:
  - `201 Created` for new todos
  - `200 OK` for successful reads/updates
  - `204 No Content` for deletions
  - `404 Not Found` when todo does not exist

## Quick start
```bash
# install dependencies
pip install -r requirements.txt

# run server
uvicorn main:app --reload

# open docs
http://127.0.0.1:8000/docs
