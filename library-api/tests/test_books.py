def _make_author(client, name="Author One", bio=None):
    r = client.post("/authors/", json={"name": name, "bio": bio})
    assert r.status_code == 201, r.text
    return r.json()

def _make_genre(client, name="sci-fi"):
    r = client.post("/genres/", json={"name": name})
    assert r.status_code == 201, r.text
    return r.json()

def test_create_book_ok_and_duplicate(client):
    a = _make_author(client, name="John")
    g = _make_genre(client, name="sci-fi")

    r_book = client.post("/books/", json={
        "title": "Title",
        "author_id": a["id"],
        "published_year": 2005,
        "pages": 50,
        "isbn": "ISBN-1546",
        "genre_ids": [g["id"]],
    })
    assert r_book.status_code == 201, r_book.text
    data = r_book.json()
    assert data["id"] >= 1
    assert data["title"] == "Title"
    assert data["author_id"] == a["id"]
    assert data["genre_ids"] == [g["id"]]

    r_dup = client.post("/books/", json={
        "title": "Another",
        "author_id": a["id"],
        "published_year": 2006,
        "pages": 120,
        "isbn": "ISBN-1546",
        "genre_ids": [g["id"]],
    })
    assert r_dup.status_code == 409, r_dup.text


def test_create_book_unknown_author_and_unknown_genre(client):
    a = _make_author(client, name="Alice")
    g = _make_genre(client, name="fantasy")

    r1 = client.post("/books/", json={
        "title": "T1",
        "author_id": 999999,
        "published_year": 2000,
        "pages": 10,
        "isbn": "X-1",
        "genre_ids": [g["id"]],
    })
    assert r1.status_code == 404, r1.text

    r2 = client.post("/books/", json={
        "title": "T2",
        "author_id": a["id"],
        "published_year": 2001,
        "pages": 20,
        "isbn": "X-2",
        "genre_ids": [g["id"], 777777],
    })
    assert r2.status_code == 404, r2.text


def test_get_book_by_id_and_404(client):
    a = _make_author(client, name="Bob")
    g = _make_genre(client, name="horror")
    rb = client.post("/books/", json={
        "title": "The Book",
        "author_id": a["id"],
        "published_year": 2010,
        "pages": 300,
        "isbn": "B-1",
        "genre_ids": [g["id"]],
    })
    assert rb.status_code == 201, rb.text
    bid = rb.json()["id"]

    r_ok = client.get(f"/books/{bid}")
    assert r_ok.status_code == 200, r_ok.text
    assert r_ok.json()["title"] == "The Book"

    r_missing = client.get("/books/999999")
    assert r_missing.status_code == 404, r_missing.text


def test_list_books_filters(client):
    a1 = _make_author(client, name="Carl")
    a2 = _make_author(client, name="Derek")
    g1 = _make_genre(client, name="mystery")
    g2 = _make_genre(client, name="drama")

    r1 = client.post("/books/", json={
        "title": "Mystery Case",
        "author_id": a1["id"],
        "published_year": 1999,
        "pages": 222,
        "isbn": "L-1",
        "genre_ids": [g1["id"]],
    })
    assert r1.status_code == 201, r1.text

    r2 = client.post("/books/", json={
        "title": "Dramatic Story",
        "author_id": a2["id"],
        "published_year": 2005,
        "pages": 123,
        "isbn": "L-2",
        "genre_ids": [g2["id"]],
    })
    assert r2.status_code == 201, r2.text

    r_q = client.get("/books/", params={"q": "Mystery"})
    assert r_q.status_code == 200, r_q.text
    titles = [b["title"] for b in r_q.json()]
    assert "Mystery Case" in titles
    assert "Dramatic Story" not in titles

    r_a = client.get("/books/", params={"author_id": a2["id"]})
    assert r_a.status_code == 200, r_a.text
    assert all(b["author_id"] == a2["id"] for b in r_a.json())

    r_g = client.get("/books/", params={"genre_id": g1["id"]})
    assert r_g.status_code == 200, r_g.text
    for b in r_g.json():
        assert g1["id"] in b["genre_ids"]


def test_patch_book_update_fields_and_genres_and_author(client):
    a_old = _make_author(client, name="Old Author")
    a_new = _make_author(client, name="New Author")
    g1 = _make_genre(client, name="adventure")
    g2 = _make_genre(client, name="biography")

    rb = client.post("/books/", json={
        "title": "Patch Me",
        "author_id": a_old["id"],
        "published_year": 2011,
        "pages": 200,
        "isbn": "PATCH-1",
        "genre_ids": [g1["id"]],
    })
    assert rb.status_code == 201, rb.text
    bid = rb.json()["id"]

    r1 = client.patch(f"/books/{bid}", json={"pages": 333, "title": "Patched"})
    assert r1.status_code == 200, r1.text
    assert r1.json()["pages"] == 333
    assert r1.json()["title"] == "Patched"

    r2 = client.patch(f"/books/{bid}", json={"genre_ids": [g2["id"]]})
    assert r2.status_code == 200, r2.text
    assert r2.json()["genre_ids"] == [g2["id"]]

    r3 = client.patch(f"/books/{bid}", json={"author_id": a_new["id"]})
    assert r3.status_code == 200, r3.text
    assert r3.json()["author_id"] == a_new["id"]

    r4 = client.patch(f"/books/{bid}", json={"author_id": 999999})
    assert r4.status_code == 404, r4.text

    r5 = client.patch(f"/books/{bid}", json={"genre_ids": [777777]})
    assert r5.status_code == 404, r5.text


def test_delete_book_then_404(client):
    a = _make_author(client, name="Temp")
    g = _make_genre(client, name="temp-genre")
    rb = client.post("/books/", json={
        "title": "To Remove",
        "author_id": a["id"],
        "published_year": 2020,
        "pages": 10,
        "isbn": "DEL-1",
        "genre_ids": [g["id"]],
    })
    assert rb.status_code == 201, rb.text
    bid = rb.json()["id"]

    r_del = client.delete(f"/books/{bid}")
    assert r_del.status_code == 204, r_del.text

    r_get = client.get(f"/books/{bid}")
    assert r_get.status_code == 404, r_get.text
