console.log("history.js loaded");

document.addEventListener("DOMContentLoaded", loadHistory);

async function loadHistory() {
  const tbody =
    document.getElementById("history-tbody") ||
    document.querySelector("#history-table tbody");

  if (!tbody) {
    console.log("tbody not found");
    return;
  }

  tbody.innerHTML = "<tr><td colspan='4'>Loading...</td></tr>";

  try {
    const res = await fetch("/checkins/api/checkins/", {
      headers: { Accept: "application/json" },
    });

    if (!res.ok) {
      tbody.innerHTML = "<tr><td colspan='4'>API error</td></tr>";
      return;
    }

    const data = await res.json();
    console.log("API DATA:", data);

    
    let items = data.items || [];
    if (Array.isArray(items) && Array.isArray(items[0])) {
      items = items.flat();
    }

    if (!items.length) {
      tbody.innerHTML = "<tr><td colspan='4'>No check-ins yet</td></tr>";
      return;
    }

    tbody.innerHTML = "";

    items.forEach((item) => {
      const row = document.createElement("tr");

      const date = item.checkin_date ?? "";
      const energy = item.energy_score ?? "";
      const mood = item.mood_score ?? "";
      const activity = item.activity_score ?? "";

      row.innerHTML = `
        <td>${date}</td>
        <td>${energy}</td>
        <td>${mood}</td>
        <td>${activity}</td>
      `;

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error(err);
    tbody.innerHTML = "<tr><td colspan='4'>Failed to load data</td></tr>";
  }
}