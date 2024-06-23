from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from gpt.gpt_chat import gpt_chat
import pymysql
import pandas as pd
from datetime import datetime 

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

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
        print(f"GPT response: {gpt_response}")
        return jsonify({'response': gpt_response})
    except Exception as e:
        print(f"Error in gpt_api: {str(e)}")
        return jsonify({'error': str(e)}), 500


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
    app.run(debug=True, port=5001)
 