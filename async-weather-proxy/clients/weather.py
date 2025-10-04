import asyncio
import random
from typing import Literal

import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def _units_to_params(units: Literal["metric", "imperial"]) -> dict:
    if units == "imperial":
        return {"temperature_unit": "fahrenheit", "wind_speed_unit": "mph"}
    return {"temperature_unit": "celsius", "wind_speed_unit": "kmh"}

async def fetch_weather(lat: float, lon: float, units: Literal["metric", "imperial"] = "metric") -> dict:
    """
    Возвращает сырые данные Open-Meteo (dict). С ретраями и таймаутом.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto",
        **_units_to_params(units),
    }

    timeout = httpx.Timeout(5.0, connect=2.0)
    headers = {"User-Agent": "async-weather-proxy/0.1"}

    # Простейшие ретраи с экспоненциальным backoff + jitter
    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
                resp = await client.get(OPEN_METEO_URL, params=params)
                resp.raise_for_status()
                return resp.json()
        except (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError) as e:
            if attempt == 2:
                raise
            delay = min(0.2 * (2 ** attempt) + random.random() / 10, 2.0)
            await asyncio.sleep(delay)

def normalize_open_meteo(raw: dict) -> dict:
    cur = raw.get("current") or {}
    return {
        "temperature": cur.get("temperature_2m"),
        "wind_speed": cur.get("wind_speed_10m"),
        "observed_at": cur.get("time"),
        "source": "open-meteo",
        "timezone": raw.get("timezone"),
    }

