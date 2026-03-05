console.log("✅ progress.js loaded - chart version");
const form = document.getElementById("progress-form");
const result = document.getElementById("progress-result");

let energyChartInstance = null;
function render(data) {
  if (!data || typeof data.count !== "number") {
    result.innerHTML = "<p>Unexpected response from server.</p>";
    return;
  }

  if (data.count === 0) {
    result.innerHTML = `<p>No check-ins in this date range.</p>`;
    
    if (energyChartInstance) {
      energyChartInstance.destroy();
      energyChartInstance = null;
    }
    return;
  }

  
  result.innerHTML = `
    <div>
      <p><strong>Range:</strong> ${data.from} → ${data.to}</p>
      <p><strong>Check-ins:</strong> ${data.count}</p>
      <ul>
        <li><strong>Average energy:</strong> ${data.averages.energy}</li>
        <li><strong>Average mood:</strong> ${data.averages.mood}</li>
        <li><strong>Average activity:</strong> ${data.averages.activity}</li>
      </ul>
    </div>
  `;

  
  const ctx = document.getElementById("energyChart").getContext("2d");
  

  if (energyChartInstance) energyChartInstance.destroy();

  energyChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Energy", "Mood", "Activity"],
      datasets: [
        {
          label: "Averages",
          data: [data.averages.energy, data.averages.mood, data.averages.activity],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { beginAtZero: true, suggestedMax: 5 } },
    },
  });
}
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const from = document.getElementById("from-date").value;
  const to = document.getElementById("to-date").value;

  if (from && to && from > to) {
    result.innerHTML = "<p>From date cannot be after To date.</p>";
    return;
  }

  const btn = document.getElementById("calcBtn");
  if (btn) btn.disabled = true;

  result.textContent = "Loading...";

  const params = new URLSearchParams();
  if (from) params.append("from", from);
  if (to) params.append("to", to);

  const url = `/checkins/api/progress/?${params.toString()}`;

  try {
    const res = await fetch(url, { headers: { Accept: "application/json" } });

    if (!res.ok) {
      result.textContent = `API error: ${res.status}`;
      return;
    }

    const data = await res.json();
    render(data);
  } catch (err) {
    result.textContent = `Error: ${err.message}`;
  } finally {
    if (btn) btn.disabled = false;
  }
});