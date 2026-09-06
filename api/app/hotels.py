"""Catálogo de hoteles reales usados en la demo.

Nombres, ciudades y coordenadas corresponden a hoteles que existen en Ecuador.
`base_price` es una aproximación a la tarifa pública vigente al momento de la
consulta (septiembre 2026, vía buscadores y agregadores de reserva) — no una
tarifa oficial confirmada con el hotel, y varía por temporada y disponibilidad.
Hacienda Zuleta, Mashpi Lodge, Sacha Lodge y Pikaia Lodge cotizan por
persona/noche en paquetes todo incluido, no por habitación; su `base_price`
es una equivalencia aproximada, no el precio total del paquete.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Hotel:
    id: str
    name: str
    city: str
    region: str  # coast | insular | sierra | amazon | urban | cloudforest
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
    Hotel(
        id="illa-experience",
        name="Illa Experience Hotel",
        city="Quito",
        region="sierra",
        lat=-0.2211,
        lon=-78.5142,
        base_price=329.0,
        search_keyword="illa experience hotel quito",
        image="img/hotels/illa-experience.jpg",
        blurb="Boutique de lujo cerca de la Plaza Santo Domingo, en el centro histórico de Quito.",
    ),
    Hotel(
        id="patio-andaluz",
        name="Patio Andaluz",
        city="Quito",
        region="sierra",
        lat=-0.2205,
        lon=-78.5136,
        base_price=130.0,
        search_keyword="hotel patio andaluz quito",
        image="img/hotels/patio-andaluz.jpg",
        blurb="Casa colonial del siglo XVI declarada monumento nacional, a pasos de la Plaza Grande.",
    ),
    Hotel(
        id="jw-marriott-quito",
        name="JW Marriott Quito",
        city="Quito",
        region="urban",
        lat=-0.1954,
        lon=-78.4867,
        base_price=200.0,
        search_keyword="jw marriott quito",
        image="img/hotels/jw-marriott-quito.jpg",
        blurb="Torre de negocios frente al parque La Carolina, en el distrito financiero de Quito.",
    ),
    Hotel(
        id="hilton-colon-quito",
        name="Hilton Colón Quito",
        city="Quito",
        region="urban",
        lat=-0.1985,
        lon=-78.4875,
        base_price=150.0,
        search_keyword="hilton colon quito",
        image="img/hotels/hilton-colon-quito.jpg",
        blurb="Uno de los hoteles de convenciones más grandes de la capital, sobre la Av. Amazonas.",
    ),
    Hotel(
        id="mashpi-lodge",
        name="Mashpi Lodge",
        city="Bosque de Mashpi (Pichincha)",
        region="cloudforest",
        lat=0.1667,
        lon=-78.8667,
        base_price=900.0,
        search_keyword="mashpi lodge ecuador",
        image="img/hotels/mashpi-lodge.jpg",
        blurb="Lodge de lujo dentro de una reserva de bosque nublado, referencia mundial en ecoturismo.",
    ),
    Hotel(
        id="hosteria-la-cienega",
        name="Hacienda La Ciénega",
        city="Lasso (Cotopaxi)",
        region="sierra",
        lat=-0.9333,
        lon=-78.6167,
        base_price=150.0,
        search_keyword="hacienda la cienega cotopaxi",
        image="img/hotels/hosteria-la-cienega.jpg",
        blurb="Hacienda colonial del siglo XVII a la vista del volcán Cotopaxi.",
    ),
    Hotel(
        id="samari-spa",
        name="Samari Spa Resort",
        city="Baños de Agua Santa",
        region="sierra",
        lat=-1.3928,
        lon=-78.4269,
        base_price=210.0,
        search_keyword="samari spa resort banos ecuador",
        image="img/hotels/samari-spa.jpg",
        blurb="Resort con spa junto a la puerta de entrada a la Amazonía, en Baños de Agua Santa.",
    ),
    Hotel(
        id="oro-verde-guayaquil",
        name="Hotel Oro Verde Guayaquil",
        city="Guayaquil",
        region="urban",
        lat=-2.1929,
        lon=-79.8871,
        base_price=90.0,
        search_keyword="hotel oro verde guayaquil",
        image="img/hotels/oro-verde-guayaquil.jpg",
        blurb="Cadena hotelera ecuatoriana histórica, en el corazón de Guayaquil.",
    ),
    Hotel(
        id="hilton-colon-guayaquil",
        name="Hilton Colón Guayaquil",
        city="Guayaquil",
        region="urban",
        lat=-2.1552,
        lon=-79.8931,
        base_price=115.0,
        search_keyword="hilton colon guayaquil",
        image="img/hotels/hilton-colon-guayaquil.jpg",
        blurb="Hotel de convenciones junto al centro de negocios de Guayaquil.",
    ),
    Hotel(
        id="wyndham-guayaquil",
        name="Wyndham Guayaquil",
        city="Guayaquil (Puerto Santa Ana)",
        region="urban",
        lat=-2.1878,
        lon=-79.8830,
        base_price=150.0,
        search_keyword="wyndham guayaquil puerto santa ana",
        image="img/hotels/wyndham-guayaquil.jpg",
        blurb="En el malecón renovado de Puerto Santa Ana, junto al río Guayas.",
    ),
    Hotel(
        id="hotel-santa-lucia",
        name="Hotel Santa Lucía",
        city="Cuenca",
        region="sierra",
        lat=-2.8987,
        lon=-79.0058,
        base_price=163.0,
        search_keyword="hotel santa lucia cuenca",
        image="img/hotels/hotel-santa-lucia.jpg",
        blurb="Edificio republicano del siglo XIX junto al Parque Calderón, centro colonial de Cuenca.",
    ),
    Hotel(
        id="pikaia-lodge",
        name="Pikaia Lodge",
        city="Santa Cruz (Galápagos)",
        region="insular",
        lat=-0.6167,
        lon=-90.3667,
        base_price=1340.0,
        search_keyword="pikaia lodge galapagos",
        image="img/hotels/pikaia-lodge.jpg",
        blurb="Lodge de lujo todo incluido en las tierras altas de Santa Cruz, con yate privado propio.",
    ),
]


def get_hotel(hotel_id: str) -> Hotel | None:
    return next((h for h in HOTELS if h.id == hotel_id), None)
