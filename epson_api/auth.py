import base64
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("EPSON_CLIENT_ID")
CLIENT_SECRET = os.getenv("EPSON_CLIENT_SECRET")
PRINTER_EMAIL = os.getenv("PRINTER_EMAIL")
AUTH_URL = "https://api.epsonconnect.com/api/1/printing/oauth2/auth/token?subject=printer"

def get_access_token():
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    base64_auth = base64.b64encode(auth_string.encode("ascii")).decode("ascii")

    headers = {
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    data = {
        'grant_type': 'password',
        'username': PRINTER_EMAIL,
        'password': ''
    }

    print(f"Sending request to {AUTH_URL}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")

    response = requests.post(AUTH_URL, headers=headers, data=data)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    if response.status_code == 200:
        return response.json()["access_token"], response.json()["subject_id"]
    else:
        raise Exception(f"Failed to get access token: {response.json()}")

if __name__ == "__main__":
    try:
        token, device_id = get_access_token()
        print(f"Access Token: {token}, Device ID: {device_id}")
    except Exception as e:
        print(e)
