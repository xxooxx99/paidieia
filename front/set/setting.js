document.addEventListener("DOMContentLoaded", () => {
  const buttons = {
    homeButton: "/paidieia/front/paideia/paideia.html",
    graphButton: "/paidieia/front/graph/graph.html",
    progressButton: "/paidieia/front/progress/progress.html",
    settingButton: "/paidieia/front/set/setting.html",
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
