//성인과 학생 페이지를 따로 만들어야 하는지
document.addEventListener("DOMContentLoaded", () => {
  const studentBtn = document.getElementById("studentBtn");
  const adultBtn = document.getElementById("adultBtn");

  if (studentBtn) {
    studentBtn.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "/front/paideia/paideia.html?type=student";
    });
  }

  if (adultBtn) {
    adultBtn.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "/front/paideia/paideia.html?type=adult";
    });
  }
});
