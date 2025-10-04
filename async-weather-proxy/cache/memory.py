# app/cache/memory.py
import time
import asyncio
from typing import Any, List, Dict

_lock = asyncio.Lock()
_store: dict[str, tuple[float, Any]] = {}  # key -> (expires_at, data)

def make_key(lat: float, lon: float, units: str) -> str:
    return f"w:{round(lat, 4)}:{round(lon, 4)}:{units}"

async def get(key: str):
    now = time.monotonic()
    async with _lock:
        item = _store.get(key)
        if not item:
            return None
        expires_at, data = item
        if expires_at < now:
            _store.pop(key, None)
            return None
        return data

async def set(key: str, value: Any, ttl_sec: int = 300):
    expires_at = time.monotonic() + ttl_sec
    async with _lock:
        _store[key] = (expires_at, value)

async def items() -> List[Dict[str, Any]]:
    """Вернуть все валидные записи кэша (с оставшимся TTL)."""
    now = time.monotonic()
    out: List[Dict[str, Any]] = []
    async with _lock:
        # лениво выкидываем протухшие и собираем актуальные
        dead = []
        for k, (expires_at, data) in _store.items():
            if expires_at < now:
                dead.append(k)
                continue
            out.append({"key": k, "expires_in": int(expires_at - now), **data})
        for k in dead:
            _store.pop(k, None)
    return out

async def clear() -> None:
    """Полностью очистить кэш."""
    async with _lock:
        _store.clear()

async def stats() -> Dict[str, int]:
    """Простая статистика по кэшу."""
    async with _lock:
        return {"size": len(_store)}
