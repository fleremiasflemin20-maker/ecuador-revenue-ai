from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import schemas
from .calendar_ec import holidays_for_year
from .calendar_ec import TOURIST_SEASONS
from .hotels import HOTELS, get_hotel
from .pricing_engine import price_range

app = FastAPI(
    title="Ecuador Revenue AI",
    description="Motor de revenue management predictivo para hoteles boutique en Ecuador.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hotels", response_model=list[schemas.HotelOut])
def list_hotels() -> list[schemas.HotelOut]:
    return [
        schemas.HotelOut(id=h.id, name=h.name, city=h.city, region=h.region, base_price=h.base_price)
        for h in HOTELS
    ]


@app.get("/pricing/{hotel_id}", response_model=list[schemas.DailyPricingOut])
def get_pricing(hotel_id: str, days: int = 30) -> list[schemas.DailyPricingOut]:
    hotel = get_hotel(hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail=f"Hotel '{hotel_id}' no encontrado")
    if not 1 <= days <= 90:
        raise HTTPException(status_code=400, detail="days debe estar entre 1 y 90")

    pricing = price_range(hotel, date.today(), days)
    return [
        schemas.DailyPricingOut(
            date=p.day,
            rule_based_price=p.rule_based_price,
            optimal_price=p.optimal_price,
            projected_occupancy=p.projected_occupancy,
            demand_score=p.demand_score,
            explanation=p.explanation,
        )
        for p in pricing
    ]


@app.get("/calendar/holidays", response_model=list[schemas.HolidayOut])
def get_holidays(year: int = date.today().year) -> list[schemas.HolidayOut]:
    holidays = holidays_for_year(year)
    return [schemas.HolidayOut(date=d, name=n) for d, n in sorted(holidays.items())]


@app.get("/calendar/seasons", response_model=list[schemas.SeasonOut])
def get_seasons() -> list[schemas.SeasonOut]:
    return [
        schemas.SeasonOut(name=s.name, region=s.region, demand_weight=s.demand_weight, note=s.note)
        for s in TOURIST_SEASONS
    ]
