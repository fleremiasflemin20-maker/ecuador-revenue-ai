// URL del backend en vivo. Actualízala cuando despliegues la API (ver README).
// Si no responde en FETCH_TIMEOUT_MS, el dashboard usa el snapshot precalculado
// en /demo/snapshot.json para no depender de que un servicio gratuito esté despierto.
const API_BASE_URL = "https://ecuador-revenue-ai-api.onrender.com";
const FETCH_TIMEOUT_MS = 3000;
