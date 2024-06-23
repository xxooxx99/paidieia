import requests

def upload_print_file(upload_uri, file_path, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, 'rb') as file:
        response = requests.post(upload_uri, headers=headers, data=file)
        print(f"Upload request URL: {upload_uri}")
        print(f"Headers: {headers}")
        print(f"File path: {file_path}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        print(f"Response headers: {response.headers}")

        if response.status_code == 200:
            print("File uploaded successfully")
        else:
            print(f"Failed to upload file: {response.status_code}")
            print(f"Failed to upload file: {response.text}")

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
            "color_mode": "color",
            "2_sided": "none",
            "reverse_order": False,
            "copies": 1,
            "collate": True
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    if response.status_code == 201:
        job_id = response.json()["id"]
        upload_uri = response.json()["upload_uri"]
        return job_id, upload_uri
    else:
        raise Exception(f"Failed to set print job: {response.json()}")

def execute_print(device_id, job_id, access_token):
    url = f"https://api.epsonconnect.com/api/1/printing/printers/{device_id}/jobs/{job_id}/print"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    print(f"Execute print request URL: {url}")
    print(f"Headers: {headers}")
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    if response.status_code == 200:
        print("Print job executed successfully")
    else:
        print(f"Failed to execute print job: {response.status_code}")
        print(f"Failed to execute print job: {response.text}")

