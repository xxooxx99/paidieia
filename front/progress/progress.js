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

  const todayDetails = document.getElementById("todayDetails");
  const todayLearning = document.getElementById("todayLearning");
  const todayQuiz = document.getElementById("todayQuiz");
  const quizToggle = document.getElementById("quiz");
  const answerRate = document.getElementById("answerRate");

  todayLearning.style.display = "block";
  todayQuiz.style.display = "none";
  answerRate.style.display = "none";

  if (todayDetails) {
    todayDetails.addEventListener("toggle", () => {
      if (todayDetails.open) {
        todayLearning.style.display = "block";
        todayQuiz.style.display = "none";
        answerRate.style.display = "none";
      } else {
        todayLearning.style.display = "none";
        todayQuiz.style.display = "none";
        answerRate.style.display = "none";
      }
    });
  }
  if (todayQuiz) {
    const quizContent = todayQuiz.textContent;
    const quizLines = quizContent.split("\n");
    let formattedQuiz = "";
    for (let line of quizLines) {
      if (line.startsWith("Question:")) {
        formattedQuiz += `<strong>${line}</strong><br>`;
      } else if (line.startsWith("Answer:")) {
        formattedQuiz += `${line}<br><br>`;
      }
    }
    todayQuiz.innerHTML = formattedQuiz;
  }

  if (quizToggle) {
    quizToggle.addEventListener("click", () => {
      todayLearning.style.display = "none";
      todayQuiz.style.display = "block";
      answerRate.style.display = "block";
    });
  }
});
