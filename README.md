# Python API Playground

This repository is a collection of small REST API projects built with **FastAPI** and **Pydantic**.  
The goal is to practice backend development concepts step by step — from basic CRUD endpoints to databases, authentication, and testing.

## Projects
- **Bookmarks API** – simple CRUD service for managing bookmarks with tags, notes, and favorite flag.
- (WIP) **Todo API** – task manager with deadlines and status.
- (WIP) **Notes API** – personal notes with search and categories.

## Topics Covered
- FastAPI basics: routes, path/query/body parameters
- Data validation with **Pydantic** (`Field`, `HttpUrl`, validators)
- CRUD patterns (create, read, update, delete)
- Pagination and filtering
- Automated tests with **pytest** and `TestClient`
- API documentation with **Swagger UI** (`/docs`)

## How to Run a Project
Each project lives in its own folder.  
To run, enter the folder and use:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
