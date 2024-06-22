from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from gpt.gpt_chat import gpt_chat

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

@app.route('/api/gpt', methods=['POST'])
def gpt_api():
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")

        age_category = data.get('ageCategory')
        subject_category = data.get('subjectCategory')
        attachment_check = data.get('attachmentCheck')
        prompt = data.get('prompt')
        request_type = data.get('requestType')
        language_setting = data.get('languageSetting')
        
        # 디버깅 출력
        print(f"Received data: {data}")
        print(f"Prompt: {prompt}")

        if not prompt:
            raise ValueError("No prompt provided")

        # GPT 모듈 호출
        gpt_response = gpt_chat(prompt, language_setting)
        
        # 응답 반환
        print(f"GPT response: {gpt_response}")
        return jsonify({'response': gpt_response})
    except Exception as e:
        print(f"Error in gpt_api: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
