# 📚 Library API

A simple **FastAPI + SQLAlchemy** project for practicing backend development and REST API design.  
It implements a small library system with **authors**, **genres**, and **books**, including CRUD operations, validation, and automated testing.

---

## 🚀 Features

- FastAPI + SQLAlchemy ORM models  
- SQLite database (auto-created)  
- CRUD for Authors, Genres, and Books  
- Relationships:
  - One-to-Many: Author → Books
  - Many-to-Many: Books ↔ Genres  
- Validation and error handling (404, 409, 422)
- Integration tests using **pytest + TestClient**
- Clean modular structure (models, schemas, routers, db)

---

## ⚙️ Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/library-api.git
cd library-api

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
# or
source venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn app.main:app --reload

Server runs at:
- http://127.0.0.1:8000

Interactive API docs:
- http://127.0.0.1:8000/docs

- http://127.0.0.1:8000/redoc

```

## 🧪 Run Tests

```bash
pytest -v

```

All endpoints are covered by integration tests.
Each test uses an isolated SQLite database created on startup.
