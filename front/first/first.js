document.addEventListener("DOMContentLoaded", () => {
  const studentBtn = document.getElementById("studentBtn");
  const adultBtn = document.getElementById("adultBtn");

  if (studentBtn) {
    studentBtn.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "/front/paideia/paideia.html?ageCategory=student";
    });
  }

  if (adultBtn) {
    adultBtn.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "/front/paideia/paideia.html?ageCategory=adult";
    });
  }
});
