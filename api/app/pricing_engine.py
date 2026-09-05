"""Motor de pricing: combina demanda contextual, señales en vivo y elasticidad.

Para cada día produce dos precios:
- `rule_based_price`: reglas de negocio transparentes (feriados, temporada, clima,
  tendencias de búsqueda) — fácil de auditar y explicar.
- `optimal_price`: precio que maximiza el ingreso esperado (precio × ocupación
  proyectada) según el modelo de elasticidad ajustado por regresión.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .demand import context_demand_index
from .demo_data import elasticity_coefficients
from .hotels import Hotel
from .signals import search_interest, weather_favorability

LIVE_SIGNAL_WEIGHT = 0.16


def _live_modifiers(hotel: Hotel) -> tuple[float, list[str]]:
    reasons: list[str] = []
    total = 0.0

    favorability = weather_favorability(hotel.lat, hotel.lon)
    total += (favorability - 0.5) * LIVE_SIGNAL_WEIGHT
    if favorability > 0.65:
        reasons.append("Pronóstico de 7 días favorable (soleado y cálido)")
    elif favorability < 0.35:
        reasons.append("Pronóstico de 7 días desfavorable (lluvia probable)")

    interest = search_interest(hotel.search_keyword)
    total += (interest - 50) / 100 * LIVE_SIGNAL_WEIGHT
    if interest > 65:
        reasons.append("Alto interés de búsqueda en Google para el destino")
    elif interest < 35:
        reasons.append("Bajo interés de búsqueda reciente")

    return total, reasons


def _optimal_price(hotel: Hotel, demand_index: float) -> tuple[float, float]:
    a, b, c = elasticity_coefficients(hotel)
    if b >= 0:
        # elasticidad inválida (no debería ocurrir con datos realistas): usar la regla
        fallback = hotel.base_price * (1 + demand_index)
        return fallback, 0.5

    intercept = a + c * demand_index
    price_star = -intercept / (2 * b)
    price_star = min(hotel.base_price * 1.9, max(hotel.base_price * 0.6, price_star))
    occupancy_star = min(0.98, max(0.10, a + b * price_star + c * demand_index))
    return round(price_star, 2), round(occupancy_star, 3)


@dataclass
class DailyPricing:
    day: date
    rule_based_price: float
    optimal_price: float
    projected_occupancy: float
    demand_score: int
    explanation: list[str]


def price_day(hotel: Hotel, d: date, live_modifiers: tuple[float, list[str]] | None = None) -> DailyPricing:
    context_index, reasons = context_demand_index(d, hotel)
    live_index, live_reasons = live_modifiers if live_modifiers is not None else _live_modifiers(hotel)

    total_index = max(-0.35, min(0.70, context_index + live_index))
    rule_price = round(hotel.base_price * (1 + total_index), 2)
    optimal, occupancy = _optimal_price(hotel, total_index)
    demand_score = int(round(min(100, max(0, 50 + total_index * 100))))

    return DailyPricing(
        day=d,
        rule_based_price=rule_price,
        optimal_price=optimal,
        projected_occupancy=occupancy,
        demand_score=demand_score,
        explanation=reasons + live_reasons,
    )


def price_range(hotel: Hotel, start: date, days: int) -> list[DailyPricing]:
    # las señales en vivo (clima/tendencias) no cambian día a día en este horizonte,
    # así que se consultan una sola vez por solicitud en vez de una vez por día.
    live = _live_modifiers(hotel)
    return [price_day(hotel, start + timedelta(days=i), live_modifiers=live) for i in range(days)]
