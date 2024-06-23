document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("gpt-form");

  form.addEventListener("submit", async function (event) {
    event.preventDefault(); // 폼 제출 기본 동작 막기
    console.log("Form submission prevented"); // 디버깅 메시지

    const ageCategory = document.getElementById("age-category").value;
    const subjectCategory = document.getElementById("subject-category").value;
    const attachmentCheck = document.getElementById("attachment-check").checked;
    const userPrompt = document.getElementById("user-prompt").value;
    const requestType = document.getElementById("request-type").value;
    const languageSetting = document.getElementById("language-setting").value;

    const requestData = {
      ageCategory: ageCategory,
      subjectCategory: subjectCategory,
      attachmentCheck: attachmentCheck,
      prompt: userPrompt,
      requestType: requestType,
      languageSetting: languageSetting,
    };

    console.log("Request data:", requestData); // 디버깅용 콘솔 출력

    try {
      const response = await fetch("http://localhost:5001/api/gpt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log("Server response:", result); // 디버깅용 콘솔 출력

      document.getElementById("response-container").innerText =
        result.response || "No response from server";
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("response-container").innerText =
        "An error occurred";
    }
  });

  async function fetchLearningData() {
    try {
      const response = await fetch("http://127.0.0.1:5001/api/learning_data");
      const data = await response.json();
      displayLearningData(data.learning_data);
    } catch (error) {
      console.error("Error fetching learning data:", error);
    }
  }

  async function fetchArticles(learningDataId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5001/api/articles/${learningDataId}`
      );
      const data = await response.json();
      displayArticles(data.articles);
    } catch (error) {
      console.error("Error fetching articles:", error);
    }
  }

  function displayLearningData(learningData) {
    const container = document.getElementById("learning-data");
    container.innerHTML = "<h2>Learning Data</h2>";
    learningData.forEach((item) => {
      const div = document.createElement("div");
      div.textContent = `ID: ${item.id}, Topic: ${item.topic}, Created At: ${item.created_at}`;
      div.style.cursor = "pointer";
      div.onclick = () => fetchArticles(item.id);
      container.appendChild(div);
    });
  }

  function displayArticles(articles) {
    const container = document.getElementById("articles");
    container.innerHTML = "<h2>Articles</h2>";
    articles.forEach((article) => {
      const div = document.createElement("div");
      div.textContent = `${article.content}`;
      container.appendChild(div);
    });
  }

  // Fetch and display learning data on page load
  fetchLearningData();
});
