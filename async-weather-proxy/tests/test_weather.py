import copy
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import main

client = TestClient(main.app)

def test_weather_ok():
    params = {"lat": 50.50, "lon": 45.45, "units": "metric"}
    r = client.get("/weather", params=params)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "temperature" in data
    assert "wind_speed" in data

def test_weather_cache_hit():
    params = {"lat": 49.00, "lon": -12.50, "units": "metric"}
    r1 = client.get("/weather", params=params)
    assert r1.status_code == 200

    r2 = client.get("/weather", params=params)
    assert r2.status_code == 200
    assert r2.json()["cached"]

def test_weather_bad():
    bad = {"lat": 50000, "lon": 50000, "units": "do-not-receive-it!!!!"}
    r = client.get("/weather", params=bad)
    assert r.status_code == 422
    data = r.json()
    assert "detail" in data


