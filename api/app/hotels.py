"""Catálogo demo de hoteles boutique ecuatorianos usados en el MVP."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Hotel:
    id: str
    name: str
    city: str
    region: str  # coast | insular | sierra
    lat: float
    lon: float
    base_price: float
    search_keyword: str


HOTELS: list[Hotel] = [
    Hotel(
        id="puerto-lopez-mar",
        name="Hostería Mirador del Pacífico",
        city="Puerto López",
        region="coast",
        lat=-1.5545,
        lon=-80.8090,
        base_price=65.0,
        search_keyword="hotel puerto lopez",
    ),
    Hotel(
        id="galapagos-ayora",
        name="Galápagos Lava Lodge",
        city="Puerto Ayora",
        region="insular",
        lat=-0.7444,
        lon=-90.3121,
        base_price=180.0,
        search_keyword="hotel galapagos",
    ),
    Hotel(
        id="quito-centro",
        name="Casa Colonial San Blas",
        city="Quito",
        region="sierra",
        lat=-0.2201,
        lon=-78.5123,
        base_price=90.0,
        search_keyword="hotel quito centro historico",
    ),
    Hotel(
        id="cuenca-rio",
        name="Posada del Río Tomebamba",
        city="Cuenca",
        region="sierra",
        lat=-2.9006,
        lon=-79.0045,
        base_price=75.0,
        search_keyword="hotel cuenca ecuador",
    ),
    Hotel(
        id="manta-malecon",
        name="Manta Beach Suites",
        city="Manta",
        region="coast",
        lat=-0.9500,
        lon=-80.7300,
        base_price=95.0,
        search_keyword="hotel manta",
    ),
]


def get_hotel(hotel_id: str) -> Hotel | None:
    return next((h for h in HOTELS if h.id == hotel_id), None)
