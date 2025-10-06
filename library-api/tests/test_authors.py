def test_create_author_ok_and_duplicate(client):
    r = client.post("/authors/", json={"name": "Dan", "bio": "Here you can see his bio"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["id"] >= 1
    assert data["name"] == "Dan"
    assert data["bio"] == "Here you can see his bio"

    r2 = client.post("/authors/", json={"name": "Dan", "bio": "Here you can see his bio"})
    assert r2.status_code == 409, r2.text


def test_get_author_id_and_404(client):
    r = client.post("/authors/", json={"name": "Daniel", "bio": "Here you can see his bio2"})
    assert r.status_code == 201, r.text
    cid = r.json()["id"]

    r2 = client.get(f"/authors/{cid}")
    assert r2.status_code == 200, r2.text
    assert r2.json()["name"] == "Daniel"

    r3 = client.get("/authors/999999")
    assert r3.status_code == 404, r3.text


def test_patch_author(client):
    r = client.post("/authors/", json={"name": "Dan", "bio": "Here you can see his bio"})
    assert r.status_code == 201, r.text
    cid = r.json()["id"]

    r2 = client.patch(f"/authors/{cid}", json={"bio": "updated"})
    assert r2.status_code == 200, r2.text
    assert r2.json()["bio"] == "updated"


def test_delete_author(client):
    r = client.post("/authors/", json={"name": "Dan", "bio": "Here you can see his bio"})
    assert r.status_code == 201, r.text
    cid = r.json()["id"]

    r2 = client.delete(f"/authors/{cid}")
    assert r2.status_code == 204, r2.text

    r3 = client.get(f"/authors/{cid}")
    assert r3.status_code == 404, r3.text


def test_get_author_filtered(client):
    client.post("/authors/", json={"name": "Dan", "bio": "Here you can see his bio"})
    r2 = client.get("/authors/", params={"q": "Da"})
    assert r2.status_code == 200, r2.text
    items = r2.json()
    assert any(a["name"] == "Dan" for a in items)


def test_authors_query_validation_422(client):
    r = client.get("/authors/", params={"q": "D"})
    assert r.status_code == 422, r.text


def test_author_name_validation_on_create(client):
    r = client.post("/authors/", json={"name": "D", "bio": "Here you can see his bio"})
    assert r.status_code == 422, r.text


def test_patch_author_duplicate(client):
    r1 = client.post("/authors/", json={"name": "Dan", "bio": "Here you can see his bio"})
    assert r1.status_code == 201, r1.text
    r2 = client.post("/authors/", json={"name": "Daniel", "bio": "Here you can see his bio"})
    assert r2.status_code == 201, r2.text

    cid = r2.json()["id"]

    r3 = client.patch(f"/authors/{cid}", json={"name": "Dan"})
    assert r3.status_code == 409, r3.text
