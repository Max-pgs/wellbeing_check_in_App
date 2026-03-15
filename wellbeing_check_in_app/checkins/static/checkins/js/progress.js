const form = document.getElementById("progress-form");
const result = document.getElementById("progress-result");
const summaryStats = document.getElementById("summary-stats");
const achievementList = document.getElementById("achievement-list");
const progressApp = document.getElementById("progress-app");
const progressBaseUrl = progressApp ? progressApp.dataset.progressUrl : "";

let progressChartInstance = null;

function destroyChart() {
  if (progressChartInstance) {
    progressChartInstance.destroy();
    progressChartInstance = null;
  }
}

function setSummary(summary) {
  summaryStats.innerHTML = `
    <div class="summary-item">
      <span>Average Energy</span>
      <strong>${summary.avg_energy ?? "--"}</strong>
    </div>
    <div class="summary-item">
      <span>Average Mood</span>
      <strong>${summary.avg_mood ?? "--"}</strong>
    </div>
    <div class="summary-item">
      <span>Average Activity</span>
      <strong>${summary.avg_activity ?? "--"}</strong>
    </div>
    <div class="summary-item">
      <span>Total Check-ins</span>
      <strong>${summary.total_checkins ?? 0}</strong>
    </div>
  `;
}

function setAchievements(achievements) {
  if (!achievements || achievements.length === 0) {
    achievementList.innerHTML = `<li>No achievements yet.</li>`;
    return;
  }

  achievementList.innerHTML = achievements
    .map((item) => `<li>${item}</li>`)
    .join("");
}

function renderChart(trends) {
  const canvas = document.getElementById("progressChart");
  const ctx = canvas.getContext("2d");

  destroyChart();

  if (!trends || trends.length === 0) {
    return;
  }

  progressChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: trends.map((item) => {
        const d = new Date(item.label);
        return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
      }),
      datasets: [
        {
          label: "Energy",
          data: trends.map((item) => item.energy),
          borderColor: "#425f4d",
          backgroundColor: "rgba(66, 95, 77, 0.08)",
          tension: 0.35,
          fill: false,
            pointRadius: 4,
            pointHoverRadius: 6
        },
        {
          label: "Mood",
          data: trends.map((item) => item.mood),
          borderColor: "#d3a16f",
          backgroundColor: "rgba(211, 161, 111, 0.08)",
          tension: 0.35,
          fill: false,
          pointRadius: 4,
          pointHoverRadius: 6
        },
        {
          label: "Activity",
          data: trends.map((item) => item.activity),
          borderColor: "#a5aea2",
          backgroundColor: "rgba(165, 174, 162, 0.08)",
          tension: 0.35,
          fill: false,
          pointRadius: 4,
          pointHoverRadius: 6
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: {
            display: false
          }
        },
        y: {
          beginAtZero: true,
          min: 0,
          max: 10,
          ticks: {
            stepSize: 1
          }
        }
      },
    },
  });
}

function renderEmpty(data) {
  result.innerHTML = `
    <p>No check-ins found for <strong>${data.from}</strong> to <strong>${data.to}</strong>.</p>
  `;
  setSummary({
    avg_energy: "--",
    avg_mood: "--",
    avg_activity: "--",
    total_checkins: 0,
  });
  setAchievements([]);
  destroyChart();
}

function render(data) {
  if (!data || !data.summary || !Array.isArray(data.trends)) {
    result.innerHTML = "<p>Unexpected response from server.</p>";
    destroyChart();
    return;
  }

  if (data.summary.total_checkins === 0) {
    renderEmpty(data);
    return;
  }

  result.innerHTML = `
    <p>
      Showing progress for <strong>${data.from}</strong> to <strong>${data.to}</strong>.
    </p>
  `;

  setSummary(data.summary);
  setAchievements(data.achievements || []);
  renderChart(data.trends);
}

async function loadProgress() {
  const from = document.getElementById("from-date").value;
  const to = document.getElementById("to-date").value;
  const btn = document.getElementById("calcBtn");

  if (from && to && from > to) {
    result.innerHTML = "<p>From date cannot be after To date.</p>";
    return;
  }

  const params = new URLSearchParams();
  if (from) params.append("from", from);
  if (to) params.append("to", to);

  const queryString = params.toString();
  const url = queryString ? `${progressBaseUrl}?${queryString}` : progressBaseUrl;

  try {
    btn.disabled = true;
    result.textContent = "Loading...";

    const response = await fetch(url, {
      headers: { Accept: "application/json" },
    });

    const data = await response.json();

    if (!response.ok) {
      result.innerHTML = `<p>${data.error || `API error: ${response.status}`}</p>`;
      destroyChart();
      return;
    }

    render(data);
  } catch (error) {
    result.innerHTML = `<p>Error: ${error.message}</p>`;
    destroyChart();
  } finally {
    btn.disabled = false;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  await loadProgress();
});

window.addEventListener("DOMContentLoaded", async () => {
  await loadProgress();
});