"""Historia sintética de ocupación/precio, usada para entrenar el modelo de elasticidad.

No hay datos reales de PMS conectados todavía (ver README, sección Roadmap), así
que generamos una historia plausible: la ocupación sube con la demanda contextual
y baja con el precio, tal como se espera en cualquier hotel real. Esto permite
demostrar el componente de IA (regresión de elasticidad) con una fuente honesta
y claramente etiquetada como simulada.
"""

from datetime import date, timedelta
from functools import lru_cache

import numpy as np

from .demand import context_demand_index
from .hotels import Hotel

HISTORY_DAYS = 730


def generate_history(hotel: Hotel) -> list[dict]:
    rng = np.random.default_rng(abs(hash(hotel.id)) % (2**32))
    start = date.today() - timedelta(days=HISTORY_DAYS)

    records = []
    for i in range(HISTORY_DAYS):
        d = start + timedelta(days=i)
        idx, _ = context_demand_index(d, hotel)
        idx_noisy = idx + rng.normal(0, 0.05)

        # Precio histórico: markup conservador y sub-óptimo (60% de la señal real),
        # que es justamente el margen de mejora que el motor de IA busca capturar.
        historical_price = hotel.base_price * (1 + 0.6 * idx)

        occupancy = 0.55 + 0.9 * idx_noisy - 0.21 * idx + rng.normal(0, 0.03)
        occupancy = float(min(0.98, max(0.10, occupancy)))

        records.append(
            {"date": d, "price": historical_price, "occupancy": occupancy, "demand_index": idx_noisy}
        )
    return records


@lru_cache(maxsize=None)
def elasticity_coefficients(hotel: Hotel) -> tuple[float, float, float]:
    """Ajusta occupancy ≈ a + b*price + c*demand_index por mínimos cuadrados."""
    records = generate_history(hotel)
    prices = np.array([r["price"] for r in records])
    idxs = np.array([r["demand_index"] for r in records])
    occ = np.array([r["occupancy"] for r in records])

    design = np.column_stack([np.ones_like(prices), prices, idxs])
    coef, *_ = np.linalg.lstsq(design, occ, rcond=None)
    return float(coef[0]), float(coef[1]), float(coef[2])
