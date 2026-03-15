document.addEventListener("DOMContentLoaded", function () {
  const sliderIds = [
    "id_energy_score",
    "id_mood_score",
    "id_activity_score"
  ];

  sliderIds.forEach((id) => {
    const input = document.getElementById(id);
    const output = document.getElementById(`${id}-value`);

    if (!input || !output) return;

    const updateValue = () => {
      output.textContent = input.value;
    };

    updateValue();
    input.addEventListener("input", updateValue);
  });
});