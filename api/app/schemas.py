from datetime import date

from pydantic import BaseModel


class HotelOut(BaseModel):
    id: str
    name: str
    city: str
    region: str
    base_price: float
    image: str
    blurb: str


class DailyPricingOut(BaseModel):
    date: date
    rule_based_price: float
    optimal_price: float
    projected_occupancy: float
    demand_score: int
    explanation: list[str]


class HolidayOut(BaseModel):
    date: date
    name: str


class SeasonOut(BaseModel):
    name: str
    region: str
    demand_weight: float
    note: str
