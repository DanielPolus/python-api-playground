import copy
import pytest
from fastapi.testclient import TestClient

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import main

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def _reset_state():
    main.BOOKMARKS.clear()
    main.NEXT_ID = 1
    yield
    main.BOOKMARKS.clear()

def _create_sample(title="Site", url="https://example.com/", tags=None, notes=None, favorite=False):
    payload = {
        "title": title,
        "url": url,
        "tags": tags or ["py"],
        "notes": notes,
    }
    r = client.post("/bookmarks", json=payload)
    assert r.status_code == 201, r.text
    return r.json()

def test_post_creates_bookmark():
    r = client.post("/bookmarks", json={
        "title": "FastAPI",
        "url": "https://fastapi.tiangolo.com/",
        "tags": ["API", "  Python  "],
        "notes": "useful"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["id"] == 1
    assert data["title"] == "FastAPI"
    assert data["url"].startswith("https://fastapi.tiangolo.com")
    assert set(data["tags"]) == {"api", "python"}
    assert data["favorite"] is False
    assert "created_at" in data

def test_get_list_contains_created_items():
    _create_sample(title="A")
    _create_sample(title="B")
    r = client.get("/bookmarks")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    assert items[0]["title"] == "B"
    assert items[1]["title"] == "A"

def test_get_by_id_ok_and_404():
    created = _create_sample(title="One")
    bid = created["id"]
    r = client.get(f"/bookmarks/{bid}")
    assert r.status_code == 200
    assert r.json()["id"] == bid

    r2 = client.get("/bookmarks/999")
    assert r2.status_code == 404

def test_patch_updates_only_sent_fields():
    created = _create_sample()
    bid = created["id"]
    r = client.patch(f"/bookmarks/{bid}", json={"notes": "updated"})
    assert r.status_code == 200
    data = r.json()
    assert data["notes"] == "updated"
    assert data["title"] == created["title"]
    assert data["tags"] == created["tags"]

def test_put_replaces_all_but_preserves_id_and_created_at():
    created = _create_sample(title="Old", url="https://old.example/", tags=["x"], notes="n")
    bid = created["id"]
    old_created_at = created["created_at"]

    r = client.put(f"/bookmarks/{bid}", json={
        "title": "New",
        "url": "https://new.example/",
        "tags": ["one", "one", "TWO"],
        "favorite": True,
        "notes": "replaced"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == bid
    assert data["created_at"] == old_created_at  # ты должен был сохранить это поле
    assert data["title"] == "New"
    assert data["url"].startswith("https://new.example")
    assert set(data["tags"]) == {"one", "two"}
    assert data["favorite"] is True
    assert data["notes"] == "replaced"

def test_delete_then_404_on_second_delete():
    created = _create_sample()
    bid = created["id"]
    r = client.delete(f"/bookmarks/{bid}")
    assert r.status_code == 204

    r2 = client.delete(f"/bookmarks/{bid}")
    assert r2.status_code == 404

def test_post_validation_errors():
    r = client.post("/bookmarks", json={"title": "Bad", "url": "not-a-url", "tags": []})
    assert r.status_code == 422

    r = client.post("/bookmarks", json={
        "title": "Too many tags",
        "url": "https://ex.com/",
        "tags": ["a", "b", "c", "d", "e", "f"]
    })
    assert r.status_code == 422

def test_list_query_filters():
    _create_sample(title="Python Guide", tags=["python"])
    _create_sample(title="Other", tags=["db"], notes="nice guide")
    r = client.get("/bookmarks?q=guide")
    assert r.status_code == 200
    titles = [x["title"] for x in r.json()]
    assert set(titles) == {"Python Guide", "Other"}
    r2 = client.get("/bookmarks?limit=1&skip=1")
    assert r2.status_code == 200
    assert len(r2.json()) == 1
