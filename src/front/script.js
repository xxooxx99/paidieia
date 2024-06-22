document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('gpt-form');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();  // 폼 제출 기본 동작 막기
        console.log("Form submission prevented");  // 디버깅 메시지

        const ageCategory = document.getElementById('age-category').value;
        const subjectCategory = document.getElementById('subject-category').value;
        const attachmentCheck = document.getElementById('attachment-check').checked;
        const userPrompt = document.getElementById('user-prompt').value;
        const requestType = document.getElementById('request-type').value;
        const languageSetting = document.getElementById('language-setting').value;

        const requestData = {
            ageCategory: ageCategory,
            subjectCategory: subjectCategory,
            attachmentCheck: attachmentCheck,
            prompt: userPrompt,
            requestType: requestType,
            languageSetting: languageSetting
        };

        console.log("Request data:", requestData);  // 디버깅용 콘솔 출력

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
            console.log("Server response:", result);  // 디버깅용 콘솔 출력
            
            document.getElementById('response-container').innerText = result.response || "No response from server";
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('response-container').innerText = 'An error occurred';
        }
    });
});
