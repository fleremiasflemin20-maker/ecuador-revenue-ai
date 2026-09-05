"""Genera web/demo/snapshot.json: una foto del motor de pricing real.

GitHub Pages es sitio estático y el backend gratuito (Render) se duerme si nadie
lo visita por un rato. Este snapshot usa el mismo motor de pricing_engine.py que
la API en vivo, así que el dashboard siempre muestra resultados reales y
consistentes mientras el backend termina de despertar.

Uso: python scripts/generate_demo_snapshot.py
"""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))

from app.calendar_ec import TOURIST_SEASONS, holidays_for_year  # noqa: E402
from app.hotels import HOTELS  # noqa: E402
from app.pricing_engine import price_range  # noqa: E402

DAYS = 45


def build_snapshot() -> dict:
    today = date.today()
    hotels_out = []
    for hotel in HOTELS:
        pricing = price_range(hotel, today, DAYS)
        hotels_out.append(
            {
                "id": hotel.id,
                "name": hotel.name,
                "city": hotel.city,
                "region": hotel.region,
                "base_price": hotel.base_price,
                "pricing": [
                    {
                        "date": p.day.isoformat(),
                        "rule_based_price": p.rule_based_price,
                        "optimal_price": p.optimal_price,
                        "projected_occupancy": p.projected_occupancy,
                        "demand_score": p.demand_score,
                        "explanation": p.explanation,
                    }
                    for p in pricing
                ],
            }
        )

    holidays = holidays_for_year(today.year) | holidays_for_year(today.year + 1)
    holidays_out = [
        {"date": d.isoformat(), "name": n} for d, n in sorted(holidays.items()) if d >= today
    ]

    seasons_out = [
        {"name": s.name, "region": s.region, "demand_weight": s.demand_weight, "note": s.note}
        for s in TOURIST_SEASONS
    ]

    return {
        "generated_at": today.isoformat(),
        "hotels": hotels_out,
        "holidays": holidays_out,
        "seasons": seasons_out,
    }


if __name__ == "__main__":
    snapshot = build_snapshot()
    out_path = ROOT / "web" / "demo" / "snapshot.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))
    print(f"Snapshot escrito en {out_path} ({len(snapshot['hotels'])} hoteles, {DAYS} días c/u)")
