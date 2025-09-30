from pydantic import BaseModel

class ValuationRequest(BaseModel):
    lat: float
    lon: float
    area_m2: float
    build_year: int
    rooms: int
    school_proximity: float

class ValuationResponse(BaseModel):
    fair_value: float
    ci_low: float
    ci_high: float
    currency: str = "SAR"
    top_factors: list = []