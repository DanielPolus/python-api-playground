from fastapi import FastAPI, HTTPException, Query
from typing import Literal
import asyncio
from fastapi import Body
from schemas import BatchWeatherIn, Coords

from clients.weather import fetch_weather, normalize_open_meteo
from cache.memory import make_key, get as cache_get, set as cache_set
from cache import memory as cache


app = FastAPI(title="Async Weather Proxy")


@app.get("/health")
async def health():
    return {"ok": True}

CACHE_TTL = 300  # seconds

async def fetch_or_cache(item: Coords) -> dict:
    key = make_key(item.lat, item.lon, item.units)
    cached = await cache_get(key)
    if cached is not None:
        return {"lat": item.lat, "lon": item.lon, "units": item.units, **cached, "cached": True}

    raw = await fetch_weather(item.lat, item.lon, item.units)
    data = normalize_open_meteo(raw)
    await cache_set(key, data, ttl_sec=CACHE_TTL)
    return {"lat": item.lat, "lon": item.lon, "units": item.units, **data, "cached": False}

@app.get("/weather")
async def weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    units: Literal["metric", "imperial"] = "metric",
):
    key = make_key(lat, lon, units)
    cached = await cache_get(key)
    if cached is not None:
        return {"lat": lat, "lon": lon, "units": units, **cached, "cached": True}

    try:
        raw = await fetch_weather(lat, lon, units)
    except Exception:
        raise HTTPException(status_code=502, detail="Upstream error")

    data = normalize_open_meteo(raw)
    await cache_set(key, data, ttl_sec=CACHE_TTL)
    return {"lat": lat, "lon": lon, "units": units, **data, "cached": False}

@app.post("/batch/weather")
async def batch_weather(payload: BatchWeatherIn = Body(...)):
    sem = asyncio.Semaphore(5)

    async def worker(item: Coords) -> dict:
        async with sem:
            try:
                return await fetch_or_cache(item)
            except Exception as e:
                return {"lat": item.lat, "lon": item.lon, "units": item.units, "error": str(e)}

    tasks = [worker(it) for it in payload.items]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    return results

@app.get("/cache/weather")
async def list_cached_weather():
    return await cache.items()

@app.delete("/cache/weather", status_code=204)
async def clear_cached_weather():
    await cache.clear()
