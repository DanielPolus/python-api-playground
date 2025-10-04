from pydantic import BaseModel, Field
from typing import List, Literal

class Coords(BaseModel):
    lat: float = Field(..., ge=-90, le=900)
    lon: float = Field(..., ge=-180, le=180)
    units: Literal["metric", "imperial"] = "metric"

class BatchWeatherIn(BaseModel):
    items: List[Coords]
