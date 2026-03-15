document.addEventListener("DOMContentLoaded", function () {
  const sliderIds = [
    "id_energy_score",
    "id_mood_score",
    "id_activity_score"
  ];

  function updateSliderValue(input, output) {
    if (!input || !output) return;
    output.textContent = input.value;
  }

  sliderIds.forEach((id) => {
    const input = document.getElementById(id);
    const output = document.getElementById(`${id}-value`);

    if (!input || !output) return;

    updateSliderValue(input, output);
    input.addEventListener("input", function () {
      updateSliderValue(input, output);
    });
  });
});