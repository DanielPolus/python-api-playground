from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional, List
from fastapi import Query
from datetime import datetime
from fastapi.responses import Response

app = FastAPI()

BOOKMARKS: List[dict] = []
NEXT_ID = 1

class BookmarkCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    url: HttpUrl
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = Field(None, max_length=500)

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        if v is None:
            return None

        if not isinstance(v, list):
            raise ValueError("tags must be a list of strings")

        normalized = []
        for t in v:
            if not isinstance(t, str):
                raise ValueError("tags must be a list of strings")
            t = t.strip().lower()
            if not (1 <= len(t) <= 20):
                raise ValueError("each tag must be 1..20 characters")
            normalized.append(t)

        seen = set()
        unique = []
        for t in normalized:
            if t not in seen:
                seen.add(t)
                unique.append(t)

        if len(unique) > 5:
            raise ValueError("no more than 5 tags allowed")

        return unique


class BookmarkOut(BaseModel):
    id: int
    title: str
    url: HttpUrl
    tags: List[str] = Field(default_factory=list)
    favorite: bool
    notes: Optional[str] = None
    created_at: datetime

class BookmarkUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    url: Optional[HttpUrl] = None
    tags: Optional[List[str]] = None
    favorite: Optional[bool] = None
    notes: Optional[str] = None

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        if v is None:
            return None

        if not isinstance(v, list):
            raise ValueError("tags must be a list of strings")

        normalized = []
        for t in v:
            if not isinstance(t, str):
                raise ValueError("tags must be a list of strings")
            t = t.strip().lower()
            if not (1 <= len(t) <= 20):
                raise ValueError("each tag must be 1..20 characters")
            normalized.append(t)

        seen = set()
        unique = []
        for t in normalized:
            if t not in seen:
                seen.add(t)
                unique.append(t)

        if len(unique) > 5:
            raise ValueError("no more than 5 tags allowed")

        return unique

class BookmarkReplace(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    url: HttpUrl
    tags: Optional[List[str]] = Field(default_factory=list)
    favorite: bool = False
    notes: Optional[str] = Field(None, max_length=500)

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        if v is None:
            return None

        if not isinstance(v, list):
            raise ValueError("tags must be a list of strings")

        normalized = []
        for t in v:
            if not isinstance(t, str):
                raise ValueError("tags must be a list of strings")
            t = t.strip().lower()
            if not (1 <= len(t) <= 20):
                raise ValueError("each tag must be 1..20 characters")
            normalized.append(t)

        seen = set()
        unique = []
        for t in normalized:
            if t not in seen:
                seen.add(t)
                unique.append(t)

        if len(unique) > 5:
            raise ValueError("no more than 5 tags allowed")

        return unique

def _find_bookmark_index(bookmark_id: int) -> int:
    for i, t in enumerate(BOOKMARKS):
        if t["id"] == bookmark_id:
            return i
    return -1

@app.get("/")
def root():
    return "Here you can find saved bookmarks and manage them however you want"

@app.post("/bookmarks", response_model=BookmarkOut, status_code=status.HTTP_201_CREATED)
def create_bookmark(payload: BookmarkCreate):
    global NEXT_ID
    bookmark = {
        "id": NEXT_ID,
        "title": payload.title,
        "url": str(payload.url),
        "tags": payload.tags,
        "favorite": False,
        "notes": payload.notes,
        "created_at": datetime.utcnow(),
    }
    BOOKMARKS.append(bookmark)
    NEXT_ID += 1
    return bookmark

@app.get("/bookmarks", response_model=List[BookmarkOut])
def list_bookmarks(
    q: Optional[str] = Query(None, min_length=1, max_length=120),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    items = BOOKMARKS.copy()

    if q:
        needle = q.lower()
        items = [
            t for t in items
            if needle in t["title"].lower()
            or (t["notes"] or "").lower().find(needle) != -1
        ]

    items = sorted(items, key=lambda t: t["id"], reverse=True)

    return items[skip : skip + limit]

@app.get("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def get_bookmark(bookmark_id: int):
    for t in BOOKMARKS:
        if t["id"] == bookmark_id:
            return t
    raise HTTPException(status_code=404, detail="Bookmark not found")

@app.patch("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def patch_bookmark(bookmark_id: int, payload: BookmarkUpdate):
    idx = _find_bookmark_index(bookmark_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    data = payload.model_dump(exclude_unset=True)

    BOOKMARKS[idx].update(data)
    return BOOKMARKS[idx]


@app.put("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def put_bookmark(bookmark_id: int, payload: BookmarkReplace):
    idx = _find_bookmark_index(bookmark_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    preserved = {
        "id": BOOKMARKS[idx]["id"],
        "created_at": BOOKMARKS[idx]["created_at"],
    }

    BOOKMARKS[idx] = {
        **preserved,
        "title": payload.title,
        "url": payload.url,
        "favorite": payload.favorite,
        "tags": payload.tags,
        "notes": payload.notes,
    }

    return BOOKMARKS[idx]

@app.delete("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def delete_bookmark(bookmark_id: int):
    idx = _find_bookmark_index(bookmark_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    BOOKMARKS.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
