#프린트 작업 실행 및 상태 확인을 처리import requests
import requests

def execute_print(device_id, job_id, access_token):
    url = f"https://api.epsonconnect.com/api/1/printing/printers/{device_id}/jobs/{job_id}/print"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    print(f"Sending request to {url}")
    print(f"Headers: {headers}")

    response = requests.post(url, headers=headers)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    if response.status_code == 200:
        print("Print job executed successfully")
    else:
        raise Exception(f"Failed to execute print job: {response.json()}")

def get_print_job_info(device_id, job_id, access_token):
    url = f'https://api.epsonconnect.com/api/1/printing/printers/{device_id}/jobs/{job_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get print job information: {response.text}")

def cancel_print_job(device_id, job_id, access_token):
    url = f'https://api.epsonconnect.com/api/1/printing/printers/{device_id}/jobs/{job_id}/cancel'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data = {
        'operated_by': 'user'
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        raise Exception(f"Failed to cancel print job: {response.text}")
