document.addEventListener("DOMContentLoaded", async function () {
  const app = document.getElementById("history-app");
  const slider = document.getElementById("history-slider");
  const emptyBox = document.getElementById("history-empty");
  const detailBox = document.getElementById("history-detail");
  const prevButton = document.getElementById("history-prev");
  const nextButton = document.getElementById("history-next");

  if (!app || !slider || !emptyBox || !detailBox) return;

  const apiUrl = app.dataset.apiUrl;
  const editTemplate = app.dataset.editTemplate || "";
  const deleteTemplate = app.dataset.deleteTemplate || "";

  const detailDateText = document.getElementById("detail-date-text");
  const detailTimeText = document.getElementById("detail-time-text");
  const detailEnergy = document.getElementById("detail-energy");
  const detailMood = document.getElementById("detail-mood");
  const detailActivity = document.getElementById("detail-activity");
  const detailNotes = document.getElementById("detail-notes");
  const timelineDateLabel = document.getElementById("timeline-date-label");
  const detailEditLink = document.getElementById("detail-edit-link");
  const detailDeleteLink = document.getElementById("detail-delete-link");

  let records = [];
  let currentIndex = 0;

  function formatDateLong(value) {
    if (!value) return "Check-in";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;

    return date.toLocaleDateString("en-GB", {
      weekday: "long",
      day: "numeric",
      month: "short"
    });
  }

  function formatDateShort(value) {
    if (!value) return "Latest";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;

    return date.toLocaleDateString("en-GB", {
      month: "short",
      day: "numeric",
      year: "numeric"
    });
  }

  function updateNavButtons() {
    if (prevButton) {
      prevButton.disabled = currentIndex <= 0;
      prevButton.setAttribute("aria-disabled", String(prevButton.disabled));
    }
    if (nextButton) {
      nextButton.disabled = currentIndex >= records.length - 1;
      nextButton.setAttribute("aria-disabled", String(nextButton.disabled));
    }
  }

  function showRecord(index) {
    const item = records[index];
    if (!item) return;

    currentIndex = index;
    slider.value = index;

    emptyBox.classList.add("hidden");
    detailBox.classList.remove("hidden");

    detailDateText.textContent = formatDateLong(item.checkin_date);
    detailTimeText.textContent = item.checkin_date
      ? `Recorded on ${formatDateShort(item.checkin_date)}`
      : "Check-in record";
    detailEnergy.textContent = item.energy_score ?? "-";
    detailMood.textContent = item.mood_score ?? "-";
    detailActivity.textContent = item.activity_score ?? "-";
    detailNotes.textContent =
      item.notes && item.notes.trim() ? item.notes : "No notes.";
    timelineDateLabel.textContent = formatDateShort(item.checkin_date);

    if (detailEditLink && editTemplate) {
      detailEditLink.href = editTemplate.replace("999999", item.id);
    }

    if (detailDeleteLink && deleteTemplate) {
      detailDeleteLink.href = deleteTemplate.replace("999999", item.id);
    }

    updateNavButtons();
  }

  try {
    const response = await fetch(apiUrl, {
      headers: { Accept: "application/json" }
    });

    if (!response.ok) {
      emptyBox.textContent = "Could not load check-in history.";
      slider.disabled = true;
      if (prevButton) prevButton.disabled = true;
      if (nextButton) nextButton.disabled = true;
      return;
    }

    const data = await response.json();
    records = Array.isArray(data.items) ? data.items : [];

    if (records.length === 0) {
      emptyBox.textContent = "No check-ins yet.";
      slider.disabled = true;
      if (prevButton) prevButton.disabled = true;
      if (nextButton) nextButton.disabled = true;
      return;
    }

    slider.min = 0;
    slider.max = records.length - 1;
    slider.value = 0;

    showRecord(0);

    slider.addEventListener("input", function () {
      showRecord(parseInt(this.value, 10));
    });

    if (prevButton) {
      prevButton.addEventListener("click", function () {
        if (currentIndex > 0) {
          showRecord(currentIndex - 1);
        }
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", function () {
        if (currentIndex < records.length - 1) {
          showRecord(currentIndex + 1);
        }
      });
    }
  } catch (error) {
    emptyBox.textContent = "Error loading history.";
    slider.disabled = true;
    if (prevButton) prevButton.disabled = true;
    if (nextButton) nextButton.disabled = true;
  }
});