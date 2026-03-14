document.addEventListener("DOMContentLoaded", async function () {
  const slider = document.getElementById("history-slider");
  const emptyBox = document.getElementById("history-empty");
  const detailBox = document.getElementById("history-detail");

  const detailDateText = document.getElementById("detail-date-text");
  const detailTimeText = document.getElementById("detail-time-text");
  const detailEnergy = document.getElementById("detail-energy");
  const detailMood = document.getElementById("detail-mood");
  const detailActivity = document.getElementById("detail-activity");
  const detailNotes = document.getElementById("detail-notes");
  const timelineDateLabel = document.getElementById("timeline-date-label");

  let records = [];

  function formatDate(value) {
    if (!value) return "Check-in";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;

    return date.toLocaleDateString("en-GB", {
      weekday: "long",
      day: "numeric",
      month: "short"
    });
  }

  function showRecord(index) {
    const item = records[index];
    if (!item) return;

    emptyBox.classList.add("hidden");
    detailBox.classList.remove("hidden");

    detailDateText.textContent = formatDate(item.checkin_date);
    detailTimeText.textContent = item.checkin_date || "Check-in record";
    detailEnergy.textContent = item.energy_score ?? "-";
    detailMood.textContent = item.mood_score ?? "-";
    detailActivity.textContent = item.activity_score ?? "-";
    detailNotes.textContent = item.notes && item.notes.trim() ? item.notes : "No notes.";
    timelineDateLabel.textContent = item.checkin_date || "Latest";
  }

  try {
    const response = await fetch("/checkins/api/history/", {
      headers: { Accept: "application/json" }
    });

    if (!response.ok) {
      emptyBox.textContent = "Could not load check-in history.";
      slider.disabled = true;
      return;
    }

    const data = await response.json();

    if (!Array.isArray(data) || data.length === 0) {
      emptyBox.textContent = "No check-ins yet.";
      slider.disabled = true;
      return;
    }

    records = data;

    slider.min = 0;
    slider.max = records.length - 1;
    slider.value = 0;

    showRecord(0);

    slider.addEventListener("input", function () {
      showRecord(parseInt(this.value, 10));
    });
  } catch (error) {
    emptyBox.textContent = "Error loading history.";
    slider.disabled = true;
  }
frontend-ui
});

main
