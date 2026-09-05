"""Señales externas en vivo: clima (Open-Meteo) y tendencias de búsqueda (Google Trends).

Ambas fuentes son gratuitas y no requieren API key. Si una señal falla o tarda
demasiado, se devuelve un valor neutro para que el pricing nunca se rompa por
una dependencia externa caída.
"""

from __future__ import annotations

import time

import httpx

_CACHE: dict[str, tuple[float, float]] = {}  # key -> (timestamp, value)
_TTL_SECONDS = 6 * 60 * 60


def _cached(key: str) -> float | None:
    entry = _CACHE.get(key)
    if entry and time.time() - entry[0] < _TTL_SECONDS:
        return entry[1]
    return None


def _store(key: str, value: float) -> None:
    _CACHE[key] = (time.time(), value)


def weather_favorability(lat: float, lon: float) -> float:
    """Devuelve 0.0-1.0: qué tan favorable es el pronóstico de 7 días para viajar.

    Combina baja probabilidad de lluvia con temperatura cálida. 0.5 = neutro
    (usado como fallback si la API no responde).
    """
    key = f"weather:{lat}:{lon}"
    cached = _cached(key)
    if cached is not None:
        return cached

    try:
        resp = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "precipitation_probability_mean,temperature_2m_max",
                "forecast_days": 7,
                "timezone": "America/Guayaquil",
            },
            timeout=4.0,
        )
        resp.raise_for_status()
        daily = resp.json()["daily"]
        rain = sum(daily["precipitation_probability_mean"]) / len(daily["precipitation_probability_mean"])
        temp = sum(daily["temperature_2m_max"]) / len(daily["temperature_2m_max"])
        rain_score = max(0.0, 1.0 - rain / 100)
        temp_score = min(1.0, max(0.0, (temp - 18) / 12))  # 18°C->0, 30°C->1
        favorability = round(0.6 * rain_score + 0.4 * temp_score, 3)
    except (httpx.HTTPError, KeyError, ZeroDivisionError):
        favorability = 0.5

    _store(key, favorability)
    return favorability


def search_interest(keyword: str) -> float:
    """Interés de búsqueda relativo (0-100) para `keyword` en Ecuador, últimos 30 días.

    Usa pytrends (no oficial, sin API key). 50 = neutro si el servicio falla
    o bloquea la solicitud, lo cual ocurre ocasionalmente con Google Trends.
    """
    key = f"trend:{keyword}"
    cached = _cached(key)
    if cached is not None:
        return cached

    interest = 50.0
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="es-EC", tz=300, timeout=(3, 5))
        pytrends.build_payload([keyword], timeframe="today 1-m", geo="EC")
        df = pytrends.interest_over_time()
        if not df.empty:
            interest = float(df[keyword].tail(7).mean())
    except Exception:
        interest = 50.0

    _store(key, interest)
    return interest
