"""Catálogo de hoteles reales usados en la demo.

Nombres, ciudades y coordenadas corresponden a hoteles que existen en Ecuador.
`base_price` es una ESTIMACIÓN de referencia para fines demostrativos, no una
tarifa publicada verificada — antes de usar esto frente a un inversor o cliente
real, confirmar la tarifa actual en el sitio oficial de cada hotel.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Hotel:
    id: str
    name: str
    city: str
    region: str  # coast | insular | sierra | amazon
    lat: float
    lon: float
    base_price: float
    search_keyword: str


HOTELS: list[Hotel] = [
    Hotel(
        id="casa-gangotena",
        name="Casa Gangotena",
        city="Quito",
        region="sierra",
        lat=-0.2201,
        lon=-78.5158,
        base_price=450.0,
        search_keyword="casa gangotena quito",
    ),
    Hotel(
        id="hacienda-zuleta",
        name="Hacienda Zuleta",
        city="Angochagua (Imbabura)",
        region="sierra",
        lat=0.2833,
        lon=-78.1667,
        base_price=220.0,
        search_keyword="hacienda zuleta",
    ),
    Hotel(
        id="mansion-alcazar",
        name="Mansión Alcázar",
        city="Cuenca",
        region="sierra",
        lat=-2.9006,
        lon=-79.0045,
        base_price=150.0,
        search_keyword="mansion alcazar cuenca",
    ),
    Hotel(
        id="casa-ceibo",
        name="Casa Ceibo Boutique Hotel & Spa",
        city="Samborondón (Guayaquil)",
        region="coast",
        lat=-1.9833,
        lon=-79.8833,
        base_price=280.0,
        search_keyword="casa ceibo hotel samborondon",
    ),
    Hotel(
        id="mantaraya-lodge",
        name="Mantaraya Lodge",
        city="Puerto López",
        region="coast",
        lat=-1.5545,
        lon=-80.8090,
        base_price=140.0,
        search_keyword="mantaraya lodge puerto lopez",
    ),
    Hotel(
        id="finch-bay",
        name="Finch Bay Galapagos Hotel",
        city="Puerto Ayora (Santa Cruz)",
        region="insular",
        lat=-0.7444,
        lon=-90.3121,
        base_price=450.0,
        search_keyword="finch bay galapagos hotel",
    ),
    Hotel(
        id="golden-bay",
        name="Golden Bay Hotel",
        city="San Cristóbal",
        region="insular",
        lat=-0.9022,
        lon=-89.6100,
        base_price=180.0,
        search_keyword="golden bay hotel galapagos",
    ),
    Hotel(
        id="sacha-lodge",
        name="Sacha Lodge",
        city="Río Napo (Amazonía)",
        region="amazon",
        lat=-0.4667,
        lon=-76.4667,
        base_price=300.0,
        search_keyword="sacha lodge ecuador",
    ),
]


def get_hotel(hotel_id: str) -> Hotel | None:
    return next((h for h in HOTELS if h.id == hotel_id), None)
