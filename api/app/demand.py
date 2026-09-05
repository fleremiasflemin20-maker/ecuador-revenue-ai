"""Índice de demanda contextual: feriados, temporada turística y día de la semana.

Es la parte determinística del modelo (no depende de APIs externas), reutilizada
tanto por el motor de pricing en vivo como por el generador de historia sintética
usado para entrenar el modelo de elasticidad.
"""

from datetime import date, timedelta

from .calendar_ec import active_seasons, holidays_for_year
from .hotels import Hotel


def context_demand_index(d: date, hotel: Hotel) -> tuple[float, list[str]]:
    """Devuelve (índice de demanda, razones legibles). Índice ~0 es demanda normal."""
    reasons: list[str] = []
    index = 0.0

    holidays = holidays_for_year(d.year)
    if d in holidays:
        index += 0.25
        reasons.append(f"Feriado nacional: {holidays[d]}")
    elif (d - timedelta(days=1)) in holidays or (d + timedelta(days=1)) in holidays:
        index += 0.10
        reasons.append("Fin de semana largo por feriado cercano")

    for season in active_seasons(d, region=hotel.region):
        index += season.demand_weight
        reasons.append(season.name)

    weekday = d.weekday()  # 0 = lunes
    if weekday == 4:
        index += 0.08
        reasons.append("Viernes: arranque de fin de semana")
    elif weekday == 5:
        index += 0.12
        reasons.append("Sábado: pico de ocupación semanal")
    elif weekday <= 2:
        index -= 0.05
        reasons.append("Entre semana: demanda base")

    return round(index, 4), reasons
