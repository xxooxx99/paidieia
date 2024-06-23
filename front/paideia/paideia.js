document.addEventListener("DOMContentLoaded", () => {
  const buttons = {
      homeButton: "/front/paideia/paideia.html",
      graphButton: "/front/graph/graph.html",
      progressButton: "/front/progress/progress.html",
      settingButton: "/front/set/setting.html",
  };

  let currentAgeCategory = localStorage.getItem("ageCategory") || "default";

  for (let [id, url] of Object.entries(buttons)) {
      const button = document.getElementById(id);
      if (button) {
          button.addEventListener("click", (e) => {
              e.preventDefault();
              if (id === "homeButton") {
                  showContent(currentAgeCategory);
              } else {
                  window.location.href = url;
              }
          });
      }
  }

  const urlParams = new URLSearchParams(window.location.search);
  const ageCategory = urlParams.get("ageCategory");

  if (ageCategory) {
      currentAgeCategory = ageCategory;
      localStorage.setItem("ageCategory", ageCategory);
  }

  showContent(currentAgeCategory);

  // 드롭다운 항목 선택 처리
  document.querySelectorAll('.dropdown-menu .dropdown-item').forEach(item => {
      item.addEventListener('click', function (e) {
          e.preventDefault();
          const dropdown = this.closest('.dropdown');
          const button = dropdown.querySelector('.btn');
          button.textContent = this.textContent;
          button.setAttribute('data-selected', this.textContent);  // 선택된 항목 저장
          // 선택한 항목에 active 클래스 추가
          dropdown.querySelectorAll('.dropdown-item').forEach(el => el.classList.remove('active'));
          this.classList.add('active');
      });
  });

  // 질문 제출 처리
  document.getElementById("questionForm").addEventListener("submit", async (e) => {
      e.preventDefault();

      const gradeCategory = getSelectedDropdownItem('#gradeCategory');
      const subjectCategory = getSelectedDropdownItem('#subjectCategory');
      const requestType = getSelectedDropdownItem('#requestType');
      const languageSetting = getSelectedDropdownItem('#languageSetting');
      const prompt = document.getElementById("questionInput").value;
      const ageCategory = localStorage.getItem("ageCategory");  // localStorage에서 ageCategory 가져오기

      console.log("Selected Items:", ageCategory, gradeCategory, subjectCategory, requestType, languageSetting);

      if (!ageCategory || !gradeCategory || !subjectCategory || !requestType || !languageSetting) {
          alert("모든 항목을 선택해주세요.");
          return;
      }

      const requestData = {
          ageCategory,
          gradeCategory,
          subjectCategory,
          requestType,
          languageSetting,
          prompt
      };

      console.log("Request Data:", requestData);

      try {
          const response = await fetch('http://localhost:5001/api/gpt', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(requestData)
          });

          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }

          const result = await response.json();
          console.log('Response from server:', result);
          document.getElementById('answerArea').innerText = result.response || "No response from server";
      } catch (error) {
          console.error('Error:', error);
          document.getElementById('answerArea').innerText = 'An error occurred';
      }
  });
});

function getSelectedDropdownItem(selector) {
  const button = document.querySelector(selector);
  if (!button) {
      return null;
  }
  const selectedItem = button.getAttribute('data-selected');
  return selectedItem ? selectedItem : null;
}

function showContent(ageCategory) {
  const studentContent = document.getElementById("studentContent");
  const adultContent = document.getElementById("adultContent");
  const defaultContent = document.getElementById("defaultContent");

  studentContent.style.display = "none";
  adultContent.style.display = "none";
  defaultContent.style.display = "none";

  if (ageCategory === "student") {
      studentContent.style.display = "block";
  } else if (ageCategory === "adult") {
      adultContent.style.display = "block";
  } else {
      defaultContent.style.display = "block";
  }
}

function searchCourses() {
  console.log("Searching courses...");
}

