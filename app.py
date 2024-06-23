from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from openai import OpenAI  # 수정된 부분
from dotenv import load_dotenv
from gptmodule.gpt.gpt_chat import gpt_chat
from datetime import datetime
import pymysql
import pandas as pd

# .env 파일 로드
load_dotenv()

app = Flask(__name__, static_folder='static')

CORS(app)  # 모든 도메인에서 접근 허용

#db 연결
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}
def get_db_connection():
    return pymysql.connect(
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )


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


     # 학습 자료 및 문제와 해설을 분리하여 추출
        lines = gpt_response.split('\n')
        contents = []
        content = ""
        for line in lines:
            if line.strip():  # 빈 줄이 아닌 경우
                if line.startswith("- "):  # 새로운 항목 시작
                    if content:
                        contents.append(content.strip())
                        content = ""
                content += line + " "
            else:
                if content:
                    contents.append(content.strip())
                    content = ""
        if content:
            contents.append(content.strip())

        # 데이터베이스 연결 및 삽입
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # learning_data 테이블에 데이터 삽입
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        topic = prompt[:50]  # 예시로 프롬프트의 앞 50자를 주제로 사용
        # category_id = subject_category  # subject_category를 category_id로 사용
        cursor.execute(
            "INSERT INTO learning_data (created_at, topic) VALUES (%s, %s)",
            (created_at,  topic)
        )
        learning_data_id = cursor.lastrowid

       # contents를 article 테이블에 삽입
        for content in contents:
            cursor.execute(
                "INSERT INTO article (content, learning_data_id) VALUES (%s, %s)",
                (content, learning_data_id)
            )

   # 변경 사항 커밋
        cnx.commit()

        cursor.close()
        cnx.close()


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
        print_server_url = 'http://localhost:5001/print'
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


@app.route('/api/articles/<int:learning_data_id>', methods=['GET'])
def get_articles(learning_data_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM article WHERE learning_data_id = %s", (learning_data_id,))
        articles = cursor.fetchall()
        cursor.close()
        cnx.close()

        return jsonify({'articles': articles})
    except Exception as e:
        print(f"Error in get_articles: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/learning_data', methods=['GET'])
def get_learning_data():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM learning_data")
        learning_data = cursor.fetchall()
        cursor.close()
        cnx.close()

        return jsonify({'learning_data': learning_data})
    except Exception as e:
        print(f"Error in get_learning_data: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
