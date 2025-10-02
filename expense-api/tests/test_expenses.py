from decimal import Decimal

def _create_category(client, name="food"):
    r = client.post("/categories", json={"name": name})
    assert r.status_code == 201, r.text
    return r.json()["id"]

def test_create_expense_with_valid_category(client):
    cid = _create_category(client, "food")

    payload = {
        "amount": "12.50",
        "currency": "usd",
        "description": "lunch",
        "category_id": cid
    }
    r = client.post("/expenses", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["id"] >= 1
    assert Decimal(str(data["amount"])) == Decimal("12.50")
    assert data["currency"] == "USD"
    assert data["category_id"] == cid

def test_create_expense_with_unknown_category_fails(client):
    payload = {
        "amount": "5.00",
        "currency": "EUR",
        "description": "coffee",
        "category_id": 99999
    }
    r = client.post("/expenses", json=payload)
    assert r.status_code in (422, 404)

def test_list_expenses_with_filters_and_pagination(client):
    cid_food = _create_category(client, "food")
    cid_tr = _create_category(client, "transport")

    client.post("/expenses", json={"amount": "10.00", "currency": "USD", "description": "taxi",  "category_id": cid_tr})
    client.post("/expenses", json={"amount": "12.50", "currency": "USD", "description": "lunch", "category_id": cid_food})
    client.post("/expenses", json={"amount": "3.20",  "currency": "USD", "description": "bus",   "category_id": cid_tr})

    r_q = client.get("/expenses?q=lu")
    assert r_q.status_code == 200
    titles = [e["description"] for e in r_q.json()]
    assert any("lunch" in (t or "") for t in titles)

    r_p = client.get("/expenses?limit=2&skip=1")
    assert r_p.status_code == 200
    assert len(r_p.json()) == 2

def test_get_and_delete_expense(client):
    cid = _create_category(client, "travel")
    created = client.post("/expenses", json={
        "amount": "99.99", "currency": "EUR", "description": "ticket", "category_id": cid
    }).json()
    eid = created["id"]

    r_get = client.get(f"/expenses/{eid}")
    assert r_get.status_code == 200
    assert r_get.json()["id"] == eid

    r_del = client.delete(f"/expenses/{eid}")
    assert r_del.status_code == 204

    r_404 = client.get(f"/expenses/{eid}")
    assert r_404.status_code == 404
