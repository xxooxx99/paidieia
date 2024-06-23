document.addEventListener("DOMContentLoaded", () => {
  const userNameDisplay = document.getElementById("userNameDisplay");
  const savedName = localStorage.getItem("userName");
  if (savedName) {
    userNameDisplay.textContent = savedName;
  }

  const buttons = {
    homeButton: "/front/paideia/paideia.html",
    graphButton: "/front/graph/graph.html",
    progressButton: "/front/progress/progress.html",
    settingButton: "/front/set/setting.html",
  };

  for (let [id, url] of Object.entries(buttons)) {
    const button = document.getElementById(id);
    if (button) {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        window.location.href = url;
      });
    }
  }
});
