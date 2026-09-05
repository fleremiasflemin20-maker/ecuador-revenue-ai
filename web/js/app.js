const state = {
  mode: null, // "live" | "demo"
  hotels: [],
  pricingCache: new Map(),
  charts: {},
};

const els = {
  status: document.getElementById("status"),
  select: document.getElementById("hotel-select"),
  cards: document.getElementById("summary-cards"),
  tableBody: document.querySelector("#pricing-table tbody"),
  explanation: document.getElementById("explanation-panel"),
};

async function fetchWithTimeout(url, ms) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  try {
    const res = await fetch(url, { signal: controller.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

async function loadSnapshot() {
  const res = await fetch("demo/snapshot.json");
  return res.json();
}

async function init() {
  try {
    const hotels = await fetchWithTimeout(`${API_BASE_URL}/hotels`, FETCH_TIMEOUT_MS);
    state.mode = "live";
    state.hotels = hotels;
    els.status.textContent = "Conectado a la API en vivo — precios, clima y tendencias en tiempo real.";
    els.status.classList.add("status-live");
  } catch (err) {
    const snapshot = await loadSnapshot();
    state.mode = "demo";
    state.hotels = snapshot.hotels;
    snapshot.hotels.forEach((h) => state.pricingCache.set(h.id, h.pricing));
    els.status.textContent = `Modo demo (backend en reposo) — última foto del motor: ${snapshot.generated_at}.`;
    els.status.classList.add("status-demo");
  }

  els.select.innerHTML = state.hotels
    .map((h) => `<option value="${h.id}">${h.name} — ${h.city}</option>`)
    .join("");
  els.select.addEventListener("change", () => renderHotel(els.select.value));

  renderHotel(state.hotels[0].id);
}

async function getPricing(hotelId) {
  if (state.pricingCache.has(hotelId)) return state.pricingCache.get(hotelId);
  const pricing = await fetchWithTimeout(`${API_BASE_URL}/pricing/${hotelId}?days=45`, FETCH_TIMEOUT_MS);
  state.pricingCache.set(hotelId, pricing);
  return pricing;
}

async function renderHotel(hotelId) {
  const hotel = state.hotels.find((h) => h.id === hotelId);
  const pricing = await getPricing(hotelId);

  renderCards(hotel, pricing);
  renderPriceChart(pricing);
  renderDemandChart(pricing);
  renderTable(pricing);
  els.explanation.innerHTML = "";
}

function renderCards(hotel, pricing) {
  const avgRule = average(pricing.map((p) => p.rule_based_price));
  const avgOptimal = average(pricing.map((p) => p.optimal_price));
  const uplift = ((avgOptimal - avgRule) / avgRule) * 100;
  const bestDay = pricing.reduce((a, b) => (b.demand_score > a.demand_score ? b : a));

  els.cards.innerHTML = `
    <div class="card">
      <span class="card-label">Precio base</span>
      <span class="card-value">$${hotel.base_price.toFixed(0)}</span>
    </div>
    <div class="card">
      <span class="card-label">Precio regla (prom. 45 días)</span>
      <span class="card-value">$${avgRule.toFixed(0)}</span>
    </div>
    <div class="card highlight">
      <span class="card-label">Precio óptimo IA (prom.)</span>
      <span class="card-value">$${avgOptimal.toFixed(0)}</span>
      <span class="card-sub">${uplift >= 0 ? "+" : ""}${uplift.toFixed(1)}% vs. regla</span>
    </div>
    <div class="card">
      <span class="card-label">Día de mayor demanda</span>
      <span class="card-value">${formatDate(bestDay.date)}</span>
      <span class="card-sub">Score ${bestDay.demand_score}/100</span>
    </div>
  `;
}

function renderPriceChart(pricing) {
  const ctx = document.getElementById("priceChart");
  const labels = pricing.map((p) => formatDate(p.date));
  const dataRule = pricing.map((p) => p.rule_based_price);
  const dataOptimal = pricing.map((p) => p.optimal_price);

  state.charts.price?.destroy();
  state.charts.price = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "Precio regla de negocio", data: dataRule, borderColor: "#7c8aff", tension: 0.3, pointRadius: 0 },
        { label: "Precio óptimo (IA)", data: dataOptimal, borderColor: "#2ee6a6", tension: 0.3, pointRadius: 0 },
      ],
    },
    options: chartOptions("$"),
  });
}

function renderDemandChart(pricing) {
  const ctx = document.getElementById("demandChart");
  const labels = pricing.map((p) => formatDate(p.date));
  const data = pricing.map((p) => p.demand_score);

  state.charts.demand?.destroy();
  state.charts.demand = new Chart(ctx, {
    type: "bar",
    data: { labels, datasets: [{ label: "Índice de demanda", data, backgroundColor: "#ffb648" }] },
    options: chartOptions(""),
  });
}

function renderTable(pricing) {
  els.tableBody.innerHTML = pricing
    .map(
      (p, i) => `
      <tr data-idx="${i}">
        <td>${formatDate(p.date)}</td>
        <td>$${p.rule_based_price.toFixed(2)}</td>
        <td class="optimal">$${p.optimal_price.toFixed(2)}</td>
        <td>${Math.round(p.projected_occupancy * 100)}%</td>
        <td>${p.demand_score}</td>
      </tr>`
    )
    .join("");

  els.tableBody.querySelectorAll("tr").forEach((row) => {
    row.addEventListener("click", () => {
      const p = pricing[Number(row.dataset.idx)];
      els.tableBody.querySelectorAll("tr").forEach((r) => r.classList.remove("selected"));
      row.classList.add("selected");
      els.explanation.innerHTML = `
        <strong>${formatDate(p.date)}</strong>
        <ul>${p.explanation.map((r) => `<li>${r}</li>`).join("") || "<li>Día sin señales especiales.</li>"}</ul>
      `;
    });
  });
}

function chartOptions(prefix) {
  return {
    responsive: true,
    interaction: { mode: "index", intersect: false },
    plugins: { legend: { labels: { color: "#c8cbe0" } } },
    scales: {
      x: { ticks: { color: "#9497b5", maxTicksLimit: 10 }, grid: { color: "#262a45" } },
      y: {
        ticks: { color: "#9497b5", callback: (v) => `${prefix}${v}` },
        grid: { color: "#262a45" },
      },
    },
  };
}

function average(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function formatDate(iso) {
  const d = new Date(`${iso}T00:00:00`);
  return d.toLocaleDateString("es-EC", { weekday: "short", day: "2-digit", month: "short" });
}

init();
