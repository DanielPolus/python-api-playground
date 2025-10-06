# 🧠 Python API Playground

📌 This repository is a collection of small, educational **FastAPI + SQLAlchemy** projects built for learning and experimentation.  
Each project focuses on one or more essential backend development concepts — from basic CRUD endpoints to database relationships, validation, and testing.  
All projects are **self-contained** in their own folders and can be run independently.

---

## 📚 Projects

- **Bookmarks API** – simple CRUD service for managing bookmarks with tags, notes, and a favorite flag.  
- **Todo API** – task manager using SQLite + SQLAlchemy with search, filtering, and pagination.  
- **Expense API** – expense tracking service with categories, currency validation, and date-based filtering.  
- **Library API** – a library management system with authors, genres, and books (one-to-many and many-to-many relations, validation, and test coverage).  
- *(More coming soon…)*

---

## 🧩 Topics Covered

- FastAPI fundamentals: routes, path/query/body parameters  
- Data validation with **Pydantic** (`Field`, `validators`, regex patterns)  
- CRUD architecture and REST conventions  
- Pagination, filtering, and query parameters  
- SQLAlchemy ORM + SQLite (relationships, foreign keys, cascading)  
- Automated testing with **pytest** and `TestClient`  
- Error handling and HTTP status codes (404, 409, 422)  
- Auto-generated API documentation via **Swagger UI** (`/docs`) and **ReDoc** (`/redoc`)

---

## ⚙️ How to Run Any Project

```bash
cd <project-folder>
python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate    # macOS / Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
