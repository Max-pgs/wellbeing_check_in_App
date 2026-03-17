// Fetch progress analytics from the backend API and update
// the summary cards, achievements list, and Chart.js line chart.

const form = document.getElementById("progress-form");
const result = document.getElementById("progress-result");
const summaryStats = document.getElementById("summary-stats");
const achievementList = document.getElementById("achievement-list");
const progressApp = document.getElementById("progress-app");
const progressBaseUrl = progressApp ? progressApp.dataset.progressUrl : "";

let progressChartInstance = null;

// Remove the existing chart instance before drawing a new one
// to avoid duplicate canvases and memory leaks.
function destroyChart() {
  if (progressChartInstance) {
    progressChartInstance.destroy();
    progressChartInstance = null;
  }
}

function daysBetween(from, to) {
  const fromDate = new Date(`${from}T00:00:00`);
  const toDate = new Date(`${to}T00:00:00`);
  const diffMs = toDate - fromDate;
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

// Render the summary statistic cards.
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

// Render simple motivational messages returned by the API.
function setAchievements(achievements) {
  if (!achievements || achievements.length === 0) {
    achievementList.innerHTML = `<li>No achievements yet.</li>`;
    return;
  }

  achievementList.innerHTML = achievements
    .map((item) => `<li>${item}</li>`)
    .join("");
}

// Format a YYYY-MM-DD string into a locale-aware short date (e.g. "Feb 20").
function formatChartDate(value) {
  if (!value) return "";
  const [year, month, day] = value.split("-");
  const safeDate = new Date(Number(year), Number(month) - 1, Number(day));
  return safeDate.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

// Draw the wellbeing trends chart using Chart.js.
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
      labels: trends.map((item) => formatChartDate(item.label)),
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

// Show the empty state when no check-ins exist in the selected date range.
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

// Render the progress page UI based on the API response data.
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
      Showing progress from <strong>${data.from}</strong> to <strong>${data.to}</strong>.
    </p>
  `;

  setSummary(data.summary);
  setAchievements(data.achievements || []);
  renderChart(data.trends);
}

// Read the selected filters, request fresh analytics data from the API,
// and refresh the progress page UI.
async function loadProgress() {
  const from = document.getElementById("from-date").value;
  const to = document.getElementById("to-date").value;
  const btn = document.getElementById("calcBtn");

  if (from && to && from > to) {
    result.innerHTML = "<p>From date cannot be after To date.</p>";
    return;
  }

  if (from && to && daysBetween(from, to) > 29) {
    result.innerHTML = "<p>Please select a date range of 30 days or less.</p>";
    destroyChart();
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

// When the form is submitted, prevent normal page reload and refresh the progress data.
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  await loadProgress();
});

// On initial page load, fetch and display progress data immediately.
window.addEventListener("DOMContentLoaded", async () => {
  await loadProgress();
});