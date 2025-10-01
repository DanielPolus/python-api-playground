# Python API Playground

📌 This repo is for learning and experimentation. The projects are intentionally simple, but cover essential backend development concepts.
The goal is to practice backend development step by step — from basic CRUD endpoints to databases, authentication, and testing.  
Each project is self-contained inside its own folder.

## Projects
- **Bookmarks API** – simple CRUD service for managing bookmarks with tags, notes, and favorite flag.
- **Todo API** – task manager using SQLite + SQLAlchemy with search and pagination.
- (WIP) **Notes API** – personal notes with categories and full-text search.
- (More coming soon…)

## Topics Covered
- FastAPI basics: routes, path/query/body parameters
- Data validation with **Pydantic** (`Field`, `HttpUrl`, custom validators)
- CRUD patterns (create, read, update, delete)
- Pagination and filtering
- SQLAlchemy ORM + SQLite
- Automated tests with **pytest** and `TestClient`
- API documentation with **Swagger UI** (`/docs`)

## How to Run a Project
Each project lives in its own folder.  
To run, enter the folder and execute:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
Then open: http://127.0.0.1:8000/docs
