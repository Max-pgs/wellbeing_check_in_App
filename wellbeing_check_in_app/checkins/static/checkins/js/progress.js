const form = document.getElementById("progress-form");
const result = document.getElementById("progress-result");

function render(data) {
  if (data.count === 0) {
    result.innerHTML = `<p>No check-ins in this date range.</p>`;
    return;
  }
  result.innerHTML = `
    <p><strong>Range:</strong> ${data.from} → ${data.to}</p>
    <p><strong>Check-ins:</strong> ${data.count}</p>
    <ul>
      <li>Average energy: ${data.averages.energy}</li>
      <li>Average mood: ${data.averages.mood}</li>
      <li>Average activity: ${data.averages.activity}</li>
    </ul>
  `;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  result.textContent = "Loading...";

  const from = document.getElementById("from-date").value;
  const to = document.getElementById("to-date").value;

  const params = new URLSearchParams();
  if (from) params.append("from", from);
  if (to) params.append("to", to);

  const url = `/checkins/api/progress/?${params.toString()}`;

  try {
    const res = await fetch(url, { headers: { Accept: "application/json" } });
    const data = await res.json();

    if (!res.ok) {
      result.innerHTML = `<p role="alert">${data.error || "Error fetching progress."}</p>`;
      return;
    }
    render(data);
  } catch (err) {
    result.innerHTML = `<p role="alert">Network error.</p>`;
  }
});