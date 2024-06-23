import os
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from fpdf import FPDF
from epson_api.auth import get_access_token

app = Flask(__name__)
CORS(app)

def upload_print_file(upload_uri, file_path, access_token):
    file_extension = file_path.split('.')[-1]
    upload_uri_with_extension = f"{upload_uri}&File=1.{file_extension}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, 'rb') as file:
        file_data = file.read()
        headers["Content-Length"] = str(len(file_data))

        response = requests.post(upload_uri_with_extension, headers=headers, data=file_data)
        print(f"Upload response status code: {response.status_code}")
        print(f"Upload response text: {response.text}")

        if response.status_code == 200:
            print("File uploaded successfully")
            return True
        else:
            raise Exception(f"Failed to upload file: {response.text}")

def set_print_job(device_id, access_token):
    url = f"https://api.epsonconnect.com/api/1/printing/printers/{device_id}/jobs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "job_name": "Test Print Job",
        "print_mode": "document",
        "print_setting": {
            "media_size": "ms_a4",
            "media_type": "mt_plainpaper",
            "borderless": False,
            "print_quality": "normal",
            "source": "auto",
            "color_mode": "mono",
            "2_sided": "none",
            "reverse_order": False,
            "copies": 1,
            "collate": True
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Set print job response status code: {response.status_code}")
    print(f"Set print job response text: {response.text}")

    if response.status_code == 201:
        job_id = response.json()["id"]
        upload_uri = response.json()["upload_uri"]
        return job_id, upload_uri
    else:
        raise Exception(f"Failed to set print job: {response.json()}")

def check_device_id_validity(device_id, access_token):
    url = f"https://api.epsonconnect.com/api/1/printing/printers/{device_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print(f"Check device ID response status code: {response.status_code}")
    print(f"Check device ID response text: {response.text}")

    if response.status_code == 200:
        return True
    else:
        raise Exception(f"Invalid device ID: {response.json()}")

def execute_print(device_id, job_id, access_token):
    url = f"https://api.epsonconnect.com/api/1/printing/printers/{device_id}/jobs/{job_id}/print"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    print(f"Execute print request URL: {url}")
    print(f"Execute print headers: {headers}")
    print(f"Execute print response status code: {response.status_code}")
    print(f"Execute print response text: {response.text}")

    if response.status_code == 200:
        print("Print job executed successfully")
    else:
        raise Exception(f"Failed to execute print job: {response.json()}")

@app.route('/print', methods=['POST'])
def print_file():
    data = request.json
    gpt_response = data.get('gptResponse')
    if not gpt_response:
        return jsonify({"error": "No response provided"}), 400

    # PDF 생성
    pdf = FPDF()
    pdf.add_page()
    font_path = os.path.join(os.path.dirname(__file__), 'NotoSans-Regular.ttf')
    pdf.add_font('NotoSans', '', font_path)
    pdf.set_font('NotoSans', '', 12)
    pdf.multi_cell(0, 10, gpt_response)

    # PDF 파일 저장
    pdf_directory = os.path.join(os.path.expanduser('~'), 'printtest')  # 홈 디렉터리의 printtest 폴더에 저장
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
    pdf_file_path = os.path.join(pdf_directory, 'response.pdf')
    pdf.output(pdf_file_path)

    # DB로 저장하는 방법 (주석처리)
    # PDF 데이터를 데이터베이스에 저장하는 로직을 추가합니다.
    # import sqlite3
    # conn = sqlite3.connect('database.db')
    # c = conn.cursor()
    # with open(pdf_file_path, 'rb') as f:
    #     pdf_data = f.read()
    # c.execute("INSERT INTO pdf_files (file_name, file_data) VALUES (?, ?)", ('response.pdf', pdf_data))
    # conn.commit()
    # conn.close()

    if not os.path.exists(pdf_file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        access_token, device_id = get_access_token()
        print(f"Access Token: {access_token}")
        print(f"Device ID: {device_id}")

        # 디바이스 ID 유효성 확인
        check_device_id_validity(device_id, access_token)
        
        job_id, upload_uri = set_print_job(device_id, access_token)
        print(f"Job ID: {job_id}")
        print(f"Upload URI: {upload_uri}")
        
        if job_id and upload_uri:
            file_uploaded = upload_print_file(upload_uri, pdf_file_path, access_token)
            if file_uploaded:
                # 상태 확인 로직 제거하고 5초 대기 후 프린트 작업 실행
                time.sleep(5)
                execute_print(device_id, job_id, access_token)
                return jsonify({"message": "Print job executed successfully"})
            else:
                return jsonify({"error": "File upload failed"}), 500
        else:
            return jsonify({"error": "Failed to set print job"}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5002)
