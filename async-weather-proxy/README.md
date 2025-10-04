# Async Weather Proxy

A small asynchronous Weather Proxy built with **FastAPI** and **httpx**.  
Fetches current weather from a public API, adds an in-memory **TTL cache**, and supports **batch** requests.

## Features
- **/health** — simple health check.
- **/weather** — get current weather by `lat`, `lon`, `units` (`metric|imperial`).
- **/batch/weather** — parallel fetching for multiple coordinates (bounded concurrency).
- **In-memory TTL cache** — fast repeat responses (`cached: true`).
- (Optional) **/cache/weather** (list) and **DELETE /cache/weather** (clear) for cache inspection.
- Validation & error handling via **Pydantic**.
- Tests with **pytest** (+ ready to mock httpx via `respx`).

## Tech Stack
- **FastAPI** — web framework  
- **httpx** — async HTTP client  
- **asyncio** — concurrency (semaphores, gather)  
- **Pydantic** — validation  
- **Pytest** — testing

## Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn app.main:app --reload
Open API docs: http://127.0.0.1:8000/docs
```

## Example Endpoints
- GET /health → {"ok": true}
- GET /weather?lat=52.52&lon=13.41&units=metric
- POST /batch/weather
- 
```bash
{
  "items": [
    { "lat": 52.52, "lon": 13.41, "units": "metric" },
    { "lat": 40.71, "lon": -74.0, "units": "imperial" }
  ]
}
```

## Running tests
```bash
pytest -v
```
