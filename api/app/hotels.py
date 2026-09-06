"""Catálogo de hoteles reales usados en la demo.

Nombres, ciudades y coordenadas corresponden a hoteles que existen en Ecuador.
`base_price` es una aproximación a la tarifa pública vigente al momento de la
consulta (septiembre 2026, vía buscadores y agregadores de reserva) — no una
tarifa oficial confirmada con el hotel, y varía por temporada y disponibilidad.
Hacienda Zuleta y Sacha Lodge cotizan por persona/noche en paquetes todo
incluido, no por habitación; su `base_price` es una equivalencia aproximada.
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
    image: str
    blurb: str


HOTELS: list[Hotel] = [
    Hotel(
        id="casa-gangotena",
        name="Casa Gangotena",
        city="Quito",
        region="sierra",
        lat=-0.2201,
        lon=-78.5158,
        base_price=420.0,
        search_keyword="casa gangotena quito",
        image="img/hotels/casa-gangotena.jpg",
        blurb="Mansión republicana de lujo frente a la Plaza San Francisco, en el centro histórico de Quito.",
    ),
    Hotel(
        id="hacienda-zuleta",
        name="Hacienda Zuleta",
        city="Angochagua (Imbabura)",
        region="sierra",
        lat=0.2833,
        lon=-78.1667,
        base_price=250.0,
        search_keyword="hacienda zuleta",
        image="img/hotels/hacienda-zuleta.jpg",
        blurb="Hacienda andina del siglo XVII, todo incluido, con cabalgatas y turismo comunitario.",
    ),
    Hotel(
        id="mansion-alcazar",
        name="Mansión Alcázar",
        city="Cuenca",
        region="sierra",
        lat=-2.9006,
        lon=-79.0045,
        base_price=95.0,
        search_keyword="mansion alcazar cuenca",
        image="img/hotels/mansion-alcazar.jpg",
        blurb="Boutique en una mansión republicana del centro colonial de Cuenca, Patrimonio de la Humanidad.",
    ),
    Hotel(
        id="casa-ceibo",
        name="Casa Ceibo Boutique Hotel & Spa",
        city="Bahía de Caráquez",
        region="coast",
        lat=-0.5951,
        lon=-80.4256,
        base_price=125.0,
        search_keyword="casa ceibo hotel bahia de caraquez",
        image="img/hotels/casa-ceibo.jpg",
        blurb="Boutique frente al estuario del río Chone, en Bahía de Caráquez, Manabí.",
    ),
    Hotel(
        id="mantaraya-lodge",
        name="Mantaraya Lodge",
        city="Puerto López",
        region="coast",
        lat=-1.5545,
        lon=-80.8090,
        base_price=73.0,
        search_keyword="mantaraya lodge puerto lopez",
        image="img/hotels/mantaraya-lodge.jpg",
        blurb="Lodge en el corazón del Parque Nacional Machalilla, zona de avistamiento de ballenas jorobadas.",
    ),
    Hotel(
        id="finch-bay",
        name="Finch Bay Galapagos Hotel",
        city="Puerto Ayora (Santa Cruz)",
        region="insular",
        lat=-0.7444,
        lon=-90.3121,
        base_price=600.0,
        search_keyword="finch bay galapagos hotel",
        image="img/hotels/finch-bay.jpg",
        blurb="Único hotel con playa privada en Galápagos, frente a la Bahía Academy en Santa Cruz.",
    ),
    Hotel(
        id="golden-bay",
        name="Golden Bay Hotel",
        city="San Cristóbal",
        region="insular",
        lat=-0.9022,
        lon=-89.6100,
        base_price=293.0,
        search_keyword="golden bay hotel galapagos",
        image="img/hotels/golden-bay.jpg",
        blurb="Frente al mar en Puerto Baquerizo Moreno, isla San Cristóbal, Galápagos.",
    ),
    Hotel(
        id="sacha-lodge",
        name="Sacha Lodge",
        city="Río Napo (Amazonía)",
        region="amazon",
        lat=-0.4667,
        lon=-76.4667,
        base_price=280.0,
        search_keyword="sacha lodge ecuador",
        image="img/hotels/sacha-lodge.jpg",
        blurb="Eco-lodge en reserva privada de 5.000 hectáreas de selva amazónica, accesible solo en canoa.",
    ),
]


def get_hotel(hotel_id: str) -> Hotel | None:
    return next((h for h in HOTELS if h.id == hotel_id), None)
