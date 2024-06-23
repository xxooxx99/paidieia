from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from openai import OpenAI  # 수정된 부분
from dotenv import load_dotenv
from gptmodule.gpt.gpt_chat import gpt_chat
from datetime import datetime

# .env 파일 로드
load_dotenv()

app = Flask(__name__, static_folder='static')

CORS(app)  # 모든 도메인에서 접근 허용

@app.route('/api/gpt', methods=['POST'])
def gpt_api():
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")

        age_category = data.get('ageCategory')
        grade_category = data.get('gradeCategory')
        subject_category = data.get('subjectCategory')
        request_type = data.get('requestType')
        language_setting = data.get('languageSetting')
        prompt = data.get('prompt')

        # 디버깅 출력
        print(f"Received data: {data}")

        if not prompt:
            raise ValueError("No prompt provided")

        # 데이터 검증
        if not all([age_category, grade_category, subject_category, request_type, language_setting, prompt]):
            raise ValueError("Some required data fields are missing")

        # GPT 모듈 호출
        gpt_response = gpt_chat(prompt, age_category, grade_category, subject_category, request_type, language_setting)

        # 응답 반환
        return jsonify({'response': gpt_response})
    
    except ValueError as e:
        print(f"ValueError in gpt_api: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Unexpected error in gpt_api: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

@app.route('/api/save', methods=['POST'])
def save_file():
    data = request.json
    content = data.get('response', '')
    file_path = 'saved_file.txt'

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    return jsonify({"message": "File saved successfully", "file_path": file_path})

@app.route('/api/print_txt', methods=['POST'])
def print_txt():
    data = request.json
    file_path = data.get('file_path')

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        print_server_url = 'http://localhost:5002/print'
        response = requests.post(print_server_url, json={'file_path': file_path})
        
        if response.status_code == 200:
            return jsonify({"message": "Print job executed successfully"})
        else:
            return jsonify({"error": "Failed to execute print job"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/front/<path:path>')
def serve_front(path):
    return send_from_directory('front', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
