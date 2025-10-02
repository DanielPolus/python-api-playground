# Python API Playground

📌 This repository is for learning and experimentation. The projects are intentionally simple but cover essential backend development concepts.  
The goal is to practice backend development step by step — from basic CRUD endpoints to databases, validation, and testing.  
Each project is self-contained inside its own folder.

## Projects
- **Bookmarks API** – simple CRUD service for managing bookmarks with tags, notes, and favorite flag.
- **Todo API** – task manager using SQLite + SQLAlchemy with search and pagination.
- **Expense API** – expense tracking service with categories, currency validation, and filtering (SQLite + SQLAlchemy + Pydantic).
- (More coming soon…)

## Topics Covered
- FastAPI basics: routes, path/query/body parameters
- Data validation with **Pydantic** (`Field`, `validators`, regex patterns)
- CRUD patterns (create, read, delete)
- Pagination and filtering
- SQLAlchemy ORM + SQLite (relations, foreign keys)
- Automated tests with **pytest** and `TestClient`
- API documentation with **Swagger UI** (`/docs`)

## How to Run a Project
Each project lives in its own folder.  
To run, enter the folder and execute:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
Then open: http://127.0.0.1:8000/docs


