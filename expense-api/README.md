# Expense API

A simple Expense Tracking REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite**.  
It supports basic **CRUD operations** for Categories and Expenses, with validation handled by **Pydantic** schemas.

## Features
- Categories: create, list (with filters), get by ID, delete.
- Expenses: create (linked to categories), list (with filters + pagination), get by ID, delete.
- Validation with Pydantic (`condecimal`, regex, custom validators).
- SQLite + SQLAlchemy ORM integration.
- Pytest-based tests for categories and expenses.

## Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for database
- [SQLite](https://www.sqlite.org/) — lightweight DB
- [Pydantic](https://docs.pydantic.dev/) — validation
- [Pytest](https://docs.pytest.org/) — testing

## Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn main:app --reload
Open API docs available at: http://127.0.0.1:8000/docs
pytest -v
