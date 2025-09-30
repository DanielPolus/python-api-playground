# Python API Playground

This repository contains mini FastAPI projects for practicing REST API development.  
The first project here is **Bookmarks API** — a simple CRUD service for managing bookmarks with tags, notes, and favorite flag.

## Features
- Create, read, update and delete bookmarks (CRUD)
- Data validation with Pydantic (e.g. `HttpUrl` for URL fields, unique normalized tags, length limits)
- Query filters: search by text, tag, favorite flag
- Pagination (skip/limit)
- Auto-generated docs at `/docs` (Swagger UI)
- Unit tests with pytest + FastAPI TestClient

## Quick start
```bash
# install dependencies
pip install -r requirements.txt

# run development server
uvicorn main:app --reload

# open docs
http://127.0.0.1:8000/docs

# run test
pytest -v
