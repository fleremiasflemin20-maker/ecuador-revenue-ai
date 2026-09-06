# Ecuador Revenue AI

Motor de **revenue management predictivo** para hoteles boutique e independientes en
Ecuador. Sugiere el precio óptimo noche a noche cruzando feriados nacionales,
temporadas turísticas locales (avistamiento de ballenas, temporada alta de
Galápagos), clima en vivo y tendencias de búsqueda — señales que las plataformas
genéricas (Booking, Expedia, PMS internacionales) no modelan para el mercado
ecuatoriano.

**Demo en vivo:** `https://fleremiasflemin20-maker.github.io/ecuador-revenue-ai/`
_(se activa automáticamente al hacer push a `main`, ver [Despliegue](#despliegue))_

## Por qué esto importa

Un hotel boutique en Puerto López pierde ingresos cuando cobra la misma tarifa
en temporada de ballenas que en un martes de mayo cualquiera. Las herramientas
de revenue management existentes están entrenadas con datos globales, no con
la estacionalidad ecuatoriana. Este proyecto demuestra un motor vertical,
explicable y barato de operar, pensado como base de un producto SaaS para
hoteles y restaurantes del país.

## Arquitectura

```
┌─────────────────────┐        ┌──────────────────────────┐
│  web/ (GitHub Pages) │──────▶│  api/ (FastAPI, Render)   │
│  Dashboard estático  │  HTTP  │  Motor de pricing         │
│  Chart.js, sin build │◀──────│  /hotels /pricing /calendar│
└─────────────────────┘        └──────────────────────────┘
         │ fallback si la API no responde en 3s
         ▼
  web/demo/snapshot.json  (generado por scripts/generate_demo_snapshot.py
                            con el mismo motor de pricing, vía GitHub Actions)
```

El backend gratuito se "duerme" tras un rato sin tráfico (limitación de los
planes free de Render). Para que la demo nunca se vea rota frente a un
inversor, el dashboard intenta la API en vivo y si no responde a tiempo usa
una foto reciente generada por el mismo motor — nunca datos inventados aparte.

## Qué es real y qué es simulado

| Señal | Estado | Fuente |
|---|---|---|
| Feriados nacionales | **Real** | Calculados algorítmicamente (Computus para Semana Santa/Carnaval) |
| Temporadas turísticas | **Real** (ventanas declaradas) | Patrones públicos de turismo (ballenas, Galápagos, vacaciones escolares) |
| Clima 7 días | **Real, en vivo** | [Open-Meteo](https://open-meteo.com) (gratis, sin API key) |
| Tendencias de búsqueda | **Real, en vivo** (best-effort) | Google Trends vía `pytrends`, con fallback neutro si Google bloquea la consulta |
| Catálogo de hoteles | Real (nombre, ciudad, ubicación) | 20 hoteles reales de Ecuador — Quito, Guayaquil, Cuenca, Baños, Cotopaxi, Mashpi, Bahía de Caráquez, Puerto López, Galápagos y Amazonía |
| Precio base por hotel | Aproximado a tarifa pública vigente (sept. 2026) | Obtenido vía buscadores/agregadores de reserva, no confirmado directamente con cada hotel — varía por temporada |
| Fotos de cada hotel | Wikimedia Commons, licencia libre | Fotos representativas del destino, no fotografía oficial del hotel (esa es propiedad de cada hotel) — créditos en `web/img/hotels/CREDITS.md` |
| Ocupación histórica / elasticidad | Simulado | Historia sintética de 2 años (ver `api/app/demo_data.py`) hasta conectar un PMS real |

## El modelo

1. **Índice de demanda contextual** (`api/app/demand.py`): feriado, temporada,
   día de la semana → un índice explicable, no una caja negra.
2. **Señales en vivo** (`api/app/signals.py`): clima y búsquedas ajustan ese
   índice con datos del momento.
3. **Precio de regla de negocio**: `precio_base × (1 + índice)` — transparente
   y auditable por el equipo del hotel.
4. **Precio óptimo por IA** (`api/app/pricing_engine.py`): se ajusta una
   regresión lineal (`ocupación ≈ a + b·precio + c·índice`) sobre la historia
   simulada y se resuelve el precio que maximiza el ingreso esperado
   (`precio × ocupación`). Es el componente de aprendizaje automático: al
   conectar datos reales de un PMS, este mismo modelo se re-entrena solo.

## Correr localmente

### API

```bash
cd api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8123
```

Probar: `curl http://localhost:8123/pricing/puerto-lopez-mar?days=10`

### Dashboard

```bash
cd web
python3 -m http.server 8080
```

Abrir `http://localhost:8080`. Si `API_BASE_URL` (en `web/js/config.js`) no
apunta a una API corriendo, usa automáticamente `web/demo/snapshot.json`.

Para regenerar ese snapshot con el motor real:

```bash
python scripts/generate_demo_snapshot.py
```

## Despliegue

**API → Render (gratis):** este repo incluye `render.yaml`. En Render:
"New +" → "Blueprint" → conectar el repo → Render detecta `render.yaml` y
despliega `api/` automáticamente. Copiar la URL resultante en
`web/js/config.js` (`API_BASE_URL`).

**Dashboard → GitHub Pages:** ya está automatizado por
`.github/workflows/deploy-pages.yml`. Al hacer push a `main`:
1. Instala las dependencias de la API.
2. Regenera `web/demo/snapshot.json` con el motor real.
3. Publica `web/` en GitHub Pages.

Solo falta activarlo una vez: **Settings → Pages → Source → GitHub Actions**
en el repositorio de GitHub.

## Roadmap

- Conectar un PMS real (Cloudbeds, SiteMinder) para reemplazar la historia
  sintética por ocupación real y re-entrenar la elasticidad periódicamente.
- Señal de vuelos hacia Quito/Guayaquil (Amadeus Self-Service API) como
  predictor adicional de demanda.
- Multi-tenant: un panel por hotel/restaurante con su propio catálogo y
  parámetros de pricing.
- Extensión a restaurantes: ingeniería de menú y predicción de demanda de
  insumos usando el mismo motor de señales contextuales.

## Estructura del repo

```
api/            Backend FastAPI — motor de pricing
  app/
    calendar_ec.py    Feriados y temporadas turísticas
    demand.py          Índice de demanda contextual
    signals.py         Clima y tendencias de búsqueda en vivo
    demo_data.py        Historia sintética + ajuste de elasticidad
    pricing_engine.py   Combina todo en el precio final
    hotels.py            Catálogo demo
    main.py               Endpoints REST
web/            Dashboard estático (GitHub Pages)
scripts/        Generador del snapshot demo
render.yaml     Blueprint de despliegue de la API
```
