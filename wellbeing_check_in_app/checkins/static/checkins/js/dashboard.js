// Populate the dashboard with summary information fetched from the API
// once the page has finished loading.

document.addEventListener("DOMContentLoaded", async function () {
  const streakEl = document.getElementById("dashboard-streak");
  const weeklyGoalEl = document.getElementById("dashboard-weekly-goal");
  const totalCheckinsEl = document.getElementById("dashboard-total-checkins");
  const recentActivityEl = document.getElementById("dashboard-recent-activity");
  const dashboardApp = document.getElementById("dashboard-app");

  // Exit early if the dashboard widgets are not present on the page.
  if (!streakEl || !weeklyGoalEl || !totalCheckinsEl || !recentActivityEl || !dashboardApp) return;

  const progressUrl = dashboardApp.dataset.progressUrl;
  const checkinsUrl = dashboardApp.dataset.checkinsUrl;

  // Exit early if the dashboard widgets are not present on the page.
  function formatRelativeLabel(dateString, index) {
    const today = new Date();
    const checkinDate = new Date(dateString);

    const todayOnly = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const checkinOnly = new Date(checkinDate.getFullYear(), checkinDate.getMonth(), checkinDate.getDate());

    const diffMs = todayOnly - checkinOnly;
    const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays > 1) return `${diffDays} days ago`;

    return `Recent item ${index + 1}`;
  }

  // Convert a stored check-in date into a user-friendly relative label.
  function calculateStreak(items) {
    if (!items || items.length === 0) return 0;

    const uniqueDates = [...new Set(items.map(item => item.checkin_date))].sort().reverse();

    let streak = 0;
    let cursor = new Date();

    for (let i = 0; i < uniqueDates.length; i += 1) {
      const cursorDate = new Date(cursor.getFullYear(), cursor.getMonth(), cursor.getDate());
      const itemDate = new Date(uniqueDates[i]);

      const normalizedItemDate = new Date(itemDate.getFullYear(), itemDate.getMonth(), itemDate.getDate());

      const diffMs = cursorDate - normalizedItemDate;
      const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

      if (diffDays === 0) {
        streak += 1;
        cursor.setDate(cursor.getDate() - 1);
      } else if (diffDays === 1 && streak === 0) {
        streak += 1;
        cursor.setDate(cursor.getDate() - 2);
      } else {
        break;
      }
    }

    return streak;
  }

  // Count how many check-ins were completed during the last 7 days.
  function calculateWeeklyGoal(items) {
    if (!items || items.length === 0) {
      return { completed: 0, target: 7 };
    }

    const today = new Date();
    const weekAgo = new Date();
    weekAgo.setDate(today.getDate() - 6);

    const completed = items.filter((item) => {
      const d = new Date(item.checkin_date);
      return d >= new Date(weekAgo.getFullYear(), weekAgo.getMonth(), weekAgo.getDate());
    }).length;

    return {
      completed,
      target: 7
    };
  }

  // Show the three most recent activity items in the dashboard.
  function renderRecentActivity(items) {
    if (!items || items.length === 0) {
      recentActivityEl.innerHTML = `
        <div class="dashboard-empty-state">No recent check-ins yet.</div>
      `;
      return;
    }

    const recentItems = items.slice(0, 3);

    recentActivityEl.innerHTML = recentItems.map((item, index) => `
      <div class="dashboard-activity-row">
        <span>${formatRelativeLabel(item.checkin_date, index)}</span>
        <span class="dashboard-activity-status">✓ Completed</span>
      </div>
    `).join("");
  }

  try {
    // Load progress summary data and recent check-ins in parallel.
    const [progressResponse, checkinsResponse] = await Promise.all([
      fetch(progressUrl, {
        headers: { Accept: "application/json" }
      }),
      fetch(checkinsUrl, {
        headers: { Accept: "application/json" }
      })
    ]);

    if (!progressResponse.ok || !checkinsResponse.ok) {
      recentActivityEl.innerHTML = `<div class="dashboard-empty-state">Could not load dashboard data.</div>`;
      return;
    }

    const progressData = await progressResponse.json();
    const checkinsData = await checkinsResponse.json();

    const summary = progressData.summary || {};
    const items = Array.isArray(checkinsData.items) ? checkinsData.items : [];

    const streak = calculateStreak(items);
    const weeklyGoal = calculateWeeklyGoal(items);
    const totalCheckins = summary.total_checkins ?? items.length ?? 0;

    // Update the dashboard summary cards with live values.
    streakEl.textContent = streak;
    weeklyGoalEl.textContent = `${weeklyGoal.completed}/${weeklyGoal.target}`;
    totalCheckinsEl.textContent = totalCheckins;

    renderRecentActivity(items);
  } catch (error) {
    // Show a safe fallback message if the dashboard data cannot be loaded.
    recentActivityEl.innerHTML = `<div class="dashboard-empty-state">Error loading dashboard.</div>`;
  }
});