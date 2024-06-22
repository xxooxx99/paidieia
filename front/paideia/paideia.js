document.addEventListener("DOMContentLoaded", () => {
  const buttons = {
    homeButton: "/front/paideia/paideia.html",
    graphButton: "/front/graph/graph.html",
    progressButton: "/front/progress/progress.html",
    settingButton: "/front/set/setting.html",
  };

  let currentUserType = localStorage.getItem("userType") || "default";

  for (let [id, url] of Object.entries(buttons)) {
    const button = document.getElementById(id);
    if (button) {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        if (id === "homeButton") {
          showContent(currentUserType);
        } else {
          window.location.href = url;
        }
      });
    }
  }

  const urlParams = new URLSearchParams(window.location.search);
  const userType = urlParams.get("type");

  if (userType) {
    currentUserType = userType;
    localStorage.setItem("userType", userType);
  }

  showContent(currentUserType);
});

function showContent(userType) {
  const studentContent = document.getElementById("studentContent");
  const adultContent = document.getElementById("adultContent");
  const defaultContent = document.getElementById("defaultContent");

  studentContent.style.display = "none";
  adultContent.style.display = "none";
  defaultContent.style.display = "none";

  if (userType === "student") {
    studentContent.style.display = "block";
  } else if (userType === "adult") {
    adultContent.style.display = "block";
  } else {
    defaultContent.style.display = "block";
  }
}

function searchCourses() {
  // Implement course search functionality
  console.log("Searching courses...");
}
