from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.authors import router as authors_router
from app.api.genres import router as genres_router
from app.api.books import router as books_router

from app.db import Base, engine
from app import models

app = FastAPI(title="Library API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(authors_router)
app.include_router(genres_router)
app.include_router(books_router)
