// Load check-in history from the API and power the timeline/slider interface
// on the history page without requiring a full page reload.

document.addEventListener("DOMContentLoaded", async function () {
  const app = document.getElementById("history-app");
  const slider = document.getElementById("history-slider");
  const emptyBox = document.getElementById("history-empty");
  const detailBox = document.getElementById("history-detail");
  const prevButton = document.getElementById("history-prev");
  const nextButton = document.getElementById("history-next");

  const dateSelect = document.getElementById("history-date-select");

  const detailDateText = document.getElementById("detail-date-text");
  const detailTimeText = document.getElementById("detail-time-text");
  const detailEnergy = document.getElementById("detail-energy");
  const detailMood = document.getElementById("detail-mood");
  const detailActivity = document.getElementById("detail-activity");
  const detailNotes = document.getElementById("detail-notes");
  const timelineDateLabel = document.getElementById("timeline-date-label");
  const detailEditLink = document.getElementById("detail-edit-link");
  const detailDeleteLink = document.getElementById("detail-delete-link");

  if (
    !app ||
    !slider ||
    !emptyBox ||
    !detailBox ||
    !detailDateText ||
    !detailTimeText ||
    !detailEnergy ||
    !detailMood ||
    !detailActivity ||
    !detailNotes ||
    !timelineDateLabel
  ) {
    return;
  }

  const apiUrl = app.dataset.apiUrl;
  const editTemplate = app.dataset.editTemplate || "";
  const deleteTemplate = app.dataset.deleteTemplate || "";

  let records = [];
  let currentIndex = 0;

  // Format dates for the main detail panel.
  function formatDateLong(value) {
    if (!value) return "Check-in";

    const [year, month, day] = value.split("-");
    const safeDate = new Date(Number(year), Number(month) - 1, Number(day));

    return safeDate.toLocaleDateString("en-GB", {
      weekday: "long",
      day: "numeric",
      month: "short",
    });
  }

  // Format dates for compact labels in the timeline UI.
  function formatDateShort(value) {
    if (!value) return "No records";

    const [year, month, day] = value.split("-");
    const safeDate = new Date(Number(year), Number(month) - 1, Number(day));

    return safeDate.toLocaleDateString("en-GB", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  }

  // Format dates for the jump-to-date dropdown.
  function formatDisplayDate(value) {
    if (!value) return "—";

    const [year, month, day] = value.split("-");
    const safeDate = new Date(Number(year), Number(month) - 1, Number(day));

    return safeDate.toLocaleDateString("en-GB", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  // Disable navigation buttons when the user reaches the start or end of the list.
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

  // Populate the dropdown with all available check-in dates in the current range.
  function populateDateSelect() {
    if (!dateSelect) return;

    dateSelect.innerHTML = "";

    records.forEach(function (record, index) {
      const option = document.createElement("option");
      option.value = String(index);
      option.textContent = formatDisplayDate(record.checkin_date);
      dateSelect.appendChild(option);
    });
  }

  // Show a clean empty state if history cannot be loaded or no records exist.
  function showEmptyState(message) {
    emptyBox.textContent = message;
    emptyBox.classList.remove("hidden");
    detailBox.classList.add("hidden");

    slider.disabled = true;

    if (dateSelect) {
      dateSelect.innerHTML = "";
      dateSelect.disabled = true;
    }

    if (prevButton) prevButton.disabled = true;
    if (nextButton) nextButton.disabled = true;
  }

  // Render one selected check-in record into the detail panel
  // and update edit/delete links for that record.
  function showRecord(index) {
    const item = records[index];
    if (!item) return;

    currentIndex = index;
    slider.value = String(index);

    if (dateSelect) {
      dateSelect.value = String(index);
    }

    emptyBox.classList.add("hidden");
    detailBox.classList.remove("hidden");

    detailDateText.textContent = formatDateLong(item.checkin_date);
    detailTimeText.textContent = `Recorded on ${formatDateShort(item.checkin_date)}`;
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

  // Fetch check-in data from the backend API.
  try {
    const response = await fetch(apiUrl, {
      headers: { Accept: "application/json" },
    });

    if (!response.ok) {
      showEmptyState("Could not load check-in history.");
      return;
    }

    const data = await response.json();
    records = Array.isArray(data.items) ? data.items : [];

    if (records.length === 0) {
      showEmptyState("No check-ins yet. Create your first wellbeing record.");
      return;
    }

    slider.disabled = false;
    slider.min = "0";
    slider.max = String(records.length - 1);

    if (dateSelect) {
      dateSelect.disabled = false;
      populateDateSelect();
    }

    showRecord(records.length - 1);

    slider.addEventListener("input", function () {
      showRecord(Number(slider.value));
    });

    if (dateSelect) {
      dateSelect.addEventListener("change", function () {
        showRecord(Number(dateSelect.value));
      });
    }

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
    console.error("History page error:", error);
    showEmptyState("Error loading history.");
  }
});