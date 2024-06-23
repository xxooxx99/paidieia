document.addEventListener("DOMContentLoaded", function () {
  const userInfoForm = document.getElementById("userInfoForm");
  const userNameInput = document.getElementById("userName");
  const infoBtn = document.querySelector(".infoBtn");
  const userNameDisplay = document.getElementById("userNameDisplay");

  // 페이지 로드 시 저장된 이름 표시
  const savedName = localStorage.getItem("userName");
  if (savedName) {
    userNameDisplay.textContent = savedName;
  }

  // 정보 저장 버튼 클릭 이벤트
  infoBtn.addEventListener("click", function (e) {
    e.preventDefault();
    const name = userNameInput.value.trim();
    if (name) {
      localStorage.setItem("userName", name);
      userNameDisplay.textContent = name;
      alert("이름이 저장되었습니다.");
    } else {
      alert("이름을 입력해주세요.");
    }
  });

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
