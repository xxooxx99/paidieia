document.addEventListener('DOMContentLoaded', function() {
    let gptResponse = localStorage.getItem('gptResponse') || '';

    if (gptResponse) {
        document.getElementById('response-container').innerText = gptResponse;
    }

    window.handleSubmit = async function(event) {
        event.preventDefault();

        const requestData = collectFormData();
        console.log("Request data:", requestData);

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
            console.log("Server response:", result);

            document.getElementById('response-container').innerText = result.response || "No response from server";
            gptResponse = result.response;
            localStorage.setItem('gptResponse', gptResponse);
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('response-container').innerText = 'An error occurred';
        }

        return false;
    };

    window.handleSave = async function(event) {
        event.preventDefault();

        if (!gptResponse) {
            alert('먼저 제출 버튼을 클릭하여 데이터를 생성하세요.');
            return false;
        }

        const requestData = collectFormData();
        requestData.response = gptResponse;
        console.log("Request data for saving:", requestData);

        try {
            const response = await fetch('http://localhost:5001/api/save', {
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
            console.log("Server response for saving:", result);

            const savedFilePath = result.file_path;
            localStorage.setItem('savedFilePath', savedFilePath);
            console.log("Saved file path:", savedFilePath);

            showSuccessMessage('저장이 완료되었습니다.');
        } catch (error) {
            console.error('Error:', error);
            showErrorMessage('An error occurred while saving the file');
        }

        return false;
    };

    window.endSession = function() {
        console.log("End session button clicked");
        localStorage.removeItem('gptResponse');
        document.getElementById('response-container').innerText = '';
        showSuccessMessage('이전 학습 데이터가 삭제되었습니다.');
    };

    window.confirmPrint = function() {
        const userConfirmed = confirm("해당 기능은 현재 EPSON 프린터기를 통해서만 지원됩니다. EPSON프린터기로 진행하시겠어요?");
        if (userConfirmed) {
            handlePrint();
        }
    };

    window.handlePrint = async function() {
        console.log("Print button clicked");

        const savedFilePath = localStorage.getItem('savedFilePath');
        console.log("File path to print:", savedFilePath);

        if (!savedFilePath) {
            alert('먼저 저장 버튼을 클릭하여 파일을 저장하세요.');
            return false;
        }

        try {
            const printResponse = await fetch('http://localhost:5001/api/print_txt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ file_path: savedFilePath })
            });

            if (!printResponse.ok) {
                throw new Error(`HTTP error! status: ${printResponse.status}`);
            }

            const printResult = await printResponse.json();
            console.log("Print response:", printResult);

            showSuccessMessage('학습 데이터 출력이 완료되었습니다.');
        } catch (error) {
            console.error('Error:', error);
            showErrorMessage('학습 데이터 출력 중 오류가 발생했습니다.');
        }

        return false;
    };

    function collectFormData() {
        const ageCategory = document.getElementById('age-category').value;
        const subjectCategory = document.getElementById('subject-category').value;
        const attachmentCheck = document.getElementById('attachment-check').checked;
        const userPrompt = document.getElementById('user-prompt').value;
        const requestType = document.getElementById('request-type').value;
        const languageSetting = document.getElementById('language-setting').value;

        return {
            ageCategory: ageCategory,
            subjectCategory: subjectCategory,
            attachmentCheck: attachmentCheck,
            prompt: userPrompt,
            requestType: requestType,
            languageSetting: languageSetting
        };
    }

    function showSuccessMessage(message) {
        const messageContainer = document.createElement('div');
        messageContainer.innerText = message;
        messageContainer.style.color = 'green';
        document.body.appendChild(messageContainer);
        setTimeout(() => {
            document.body.removeChild(messageContainer);
        }, 3000);
    }

    function showErrorMessage(message) {
        const messageContainer = document.createElement('div');
        messageContainer.innerText = message;
        messageContainer.style.color = 'red';
        document.body.appendChild(messageContainer);
        setTimeout(() => {
            document.body.removeChild(messageContainer);
        }, 3000);
    }
});
