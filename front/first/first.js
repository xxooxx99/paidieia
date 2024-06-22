// $(document).ready(function () {
//   $("#studentBtn").click(function () {
//     showStudentContent();
//   });

//   $("#adultBtn").click(function () {
//     showAdultContent();
//   });
// });

// function showStudentContent() {
//   // 학생용 콘텐츠로 변경
//   $(".backGroundCard").html(`
//         <h2>학생 선택</h2>
//         <button id="elementary">초등학생</button>
//         <button id="middle">중학생</button>
//         <button id="high">고등학생</button>
//         <p>설정에서 언제든지 수정할 수 있습니다.</p>
//     `);
// }

// function showAdultContent() {
//   // 성인용 콘텐츠로 변경
//   $(".backGroundCard").html(`
//         <h2>배우고 싶은 과목 선택</h2>
//         <select id="subjectSelect">
//             <option value="">과목을 선택하세요</option>
//             <option value="math">수학</option>
//             <option value="science">과학</option>
//             <option value="language">언어</option>
//             <!-- 추가 과목들 -->
//         </select>
//     `);
// }
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
