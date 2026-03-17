// Toggle the mobile navigation menu on smaller screens.
document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.getElementById("navToggle");
  const mobileMenu = document.getElementById("mobileMenu");

  // Toggle the mobile navigation menu on smaller screens.
  if (!navToggle || !mobileMenu) return;

  navToggle.addEventListener("click", function () {
    const isOpen = mobileMenu.classList.toggle("open");
    navToggle.classList.toggle("active", isOpen);
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
});