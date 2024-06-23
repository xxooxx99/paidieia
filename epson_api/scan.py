import requests
from epson_api.auth import get_access_token

def set_scan_job(printer_id, access_token):
    url = f'https://api.epsonconnect.com/api/1/printing/printers/{printer_id}/scans'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data = {
        'scan_setting': {
            'resolution': '300dpi',
            'color_mode': 'color',
            'document_source': 'document_table',
            'file_format': 'pdf'
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()['id'], response.json()['scan_data_uri']
    else:
        raise Exception(f"Failed to set scan job: {response.json()}")

def execute_scan_job(printer_id, scan_job_id, access_token):
    url = f'https://api.epsonconnect.com/api/1/printing/printers/{printer_id}/scans/{scan_job_id}/execute'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()['scan_file_uri']
    else:
        raise Exception(f"Failed to execute scan job: {response.json()}")

def save_scanned_text(scan_file_uri, output_file_path):
    response = requests.get(scan_file_uri)
    if response.status_code == 200:
        with open(output_file_path, 'wb') as file:
            file.write(response.content)
        print(f"Scanned text saved to {output_file_path}")
    else:
        raise Exception(f"Failed to download scanned file: {response.json()}")

if __name__ == "__main__":
    printer_id = "your_printer_id"
    access_token = get_access_token()
    scan_job_id, scan_data_uri = set_scan_job(printer_id, access_token)
    scan_file_uri = execute_scan_job(printer_id, scan_job_id, access_token)
    save_scanned_text(scan_file_uri, "scanned_document.pdf")
