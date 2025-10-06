def test_create_genre_ok_and_duplicate(client):
    r = client.post("/genres/", json={"name": "horror"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["id"] >= 1
    assert data["name"] == "horror"

    r2 = client.post("/genres/", json={"name": "horror"})
    assert r2.status_code == 409, r2.text


def test_get_genre_id_and_404(client):
    r = client.post("/genres/", json={"name": "horror"})
    assert r.status_code == 201, r.text
    cid = r.json()["id"]

    r2 = client.get(f"/genres/{cid}")
    assert r2.status_code == 200, r2.text
    assert r2.json()["name"] == "horror"

    r3 = client.get("/genres/999999")
    assert r3.status_code == 404, r3.text


def test_patch_genre_ok_and_duplicate(client):
    r = client.post("/genres/", json={"name": "horror"})
    assert r.status_code == 201, r.text
    cid = r.json()["id"]

    r2 = client.patch(f"/genres/{cid}", json={"name": "sci-fi"})
    assert r2.status_code == 200, r2.text
    assert r2.json()["name"] == "sci-fi"

    r_new = client.post("/genres/", json={"name": "horror"})
    assert r_new.status_code == 201, r_new.text
    cid2 = r_new.json()["id"]

    r3 = client.patch(f"/genres/{cid2}", json={"name": "sci-fi"})
    assert r3.status_code == 409, r3.text


def test_delete_genre_id(client):
    r = client.post("/genres/", json={"name": "sci-fi"})
    assert r.status_code == 201, r.text
    cid = r.json()["id"]

    r2 = client.delete(f"/genres/{cid}")
    assert r2.status_code == 204, r2.text

    r3 = client.get(f"/genres/{cid}")
    assert r3.status_code == 404, r3.text
