def test_create_category_and_get_list(client):
    r = client.post("/categories", json={"name": "food"})
    assert r.status_code == 201, r.text
    cat = r.json()
    assert cat["id"] >= 1
    assert cat["name"] == "Food"

    r2 = client.get("/categories")
    assert r2.status_code == 200
    items = r2.json()
    assert any(c["name"] == "Food" for c in items)

def test_get_category_by_id_and_404(client):
    created = client.post("/categories", json={"name": "transport"}).json()
    cid = created["id"]

    r_ok = client.get(f"/categories/{cid}")
    assert r_ok.status_code == 200
    assert r_ok.json()["name"] == "Transport"

    r_404 = client.get("/categories/99999")
    assert r_404.status_code == 404

def test_duplicate_category_conflict(client):
    r1 = client.post("/categories", json={"name": "books"})
    assert r1.status_code == 201
    r2 = client.post("/categories", json={"name": "books"})
    assert r2.status_code in (409, 400, 422)
