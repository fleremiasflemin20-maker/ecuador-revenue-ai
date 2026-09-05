"""Calendario ecuatoriano: feriados nacionales y ventanas de temporada turística.

Los feriados fijos y la Pascua (calculada con el algoritmo de Computus) están
verificados contra el calendario oficial ecuatoriano. Las ventanas de temporada
turística reflejan patrones de demanda públicamente conocidos (avistamiento de
ballenas en Manabí, temporada alta de Galápagos, vacaciones escolares) y sirven
como señal de negocio, no como fuente legal.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


def easter_sunday(year: int) -> date:
    """Domingo de Pascua para `year`, algoritmo de Computus (gregoriano)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def holidays_for_year(year: int) -> dict[date, str]:
    """Feriados nacionales de Ecuador para `year`."""
    easter = easter_sunday(year)
    fixed = {
        date(year, 1, 1): "Año Nuevo",
        date(year, 5, 1): "Día del Trabajo",
        date(year, 5, 24): "Batalla de Pichincha",
        date(year, 8, 10): "Primer Grito de Independencia",
        date(year, 10, 9): "Independencia de Guayaquil",
        date(year, 11, 2): "Día de los Difuntos",
        date(year, 11, 3): "Independencia de Cuenca",
        date(year, 12, 25): "Navidad",
    }
    movable = {
        easter - timedelta(days=48): "Carnaval (lunes)",
        easter - timedelta(days=47): "Carnaval (martes)",
        easter - timedelta(days=2): "Viernes Santo",
    }
    return {**fixed, **movable}


@dataclass(frozen=True)
class Season:
    key: str
    name: str
    region: str
    start_month_day: tuple[int, int]
    end_month_day: tuple[int, int]
    demand_weight: float  # multiplicador adicional de demanda, ej. 0.20 = +20%
    note: str


TOURIST_SEASONS: list[Season] = [
    Season(
        key="whale_watching",
        name="Avistamiento de ballenas jorobadas",
        region="coast",
        start_month_day=(6, 1),
        end_month_day=(9, 30),
        demand_weight=0.20,
        note="Pico de visitantes a Puerto López y el Parque Nacional Machalilla.",
    ),
    Season(
        key="galapagos_high",
        name="Temporada alta Galápagos",
        region="insular",
        start_month_day=(6, 15),
        end_month_day=(9, 15),
        demand_weight=0.18,
        note="Mejor visibilidad submarina y clima templado en las islas.",
    ),
    Season(
        key="galapagos_high_dec",
        name="Temporada alta Galápagos (fin de año)",
        region="insular",
        start_month_day=(12, 15),
        end_month_day=(1, 15),
        demand_weight=0.22,
        note="Vacaciones de fin de año, alta demanda de cruceros y hoteles.",
    ),
    Season(
        key="sierra_school_break",
        name="Vacaciones escolares Sierra",
        region="sierra",
        start_month_day=(7, 1),
        end_month_day=(8, 31),
        demand_weight=0.12,
        note="Turismo interno familiar hacia Costa e Insular.",
    ),
    Season(
        key="costa_school_break",
        name="Vacaciones escolares Costa",
        region="coast",
        start_month_day=(2, 1),
        end_month_day=(3, 31),
        demand_weight=0.10,
        note="Turismo interno familiar hacia Sierra y feriados de Carnaval.",
    ),
]


def _in_window(d: date, start_md: tuple[int, int], end_md: tuple[int, int]) -> bool:
    start = date(d.year, *start_md)
    end = date(d.year, *end_md)
    if start <= end:
        return start <= d <= end
    # ventana cruza fin de año (ej. dic-ene)
    return d >= start or d <= end


def active_seasons(d: date, region: str | None = None) -> list[Season]:
    matches = [s for s in TOURIST_SEASONS if _in_window(d, s.start_month_day, s.end_month_day)]
    if region:
        matches = [s for s in matches if s.region == region]
    return matches
