import os
import csv
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def extract_text_from_pdf(pdf_path, start_page=0, end_page=None):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        end_page = end_page if end_page is not None else len(reader.pages)
        for page in range(start_page, end_page):
            text += reader.pages[page].extract_text()
    return text

def save_text_to_csv(text, csv_path):
    lines = text.split('\n')
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['word'])  # 헤더 작성
        for line in lines:
            if line.strip():  # 공백 행 제외
                writer.writerow([line.strip()])

def pdf_to_csv(pdf_path, csv_path, start_page=0, end_page=None):
    text = extract_text_from_pdf(pdf_path, start_page, end_page)
    save_text_to_csv(text, csv_path)
    print(f"PDF 데이터가 {csv_path}로 변환되었습니다.")

# 테스트 예제
if __name__ == '__main__':
    base_path = r'Z:\epson\project\paidieia\backend'
    pdf_path = os.path.join(base_path, 'testdata', '영어단어.pdf')
    csv_path = os.path.join(base_path, 'resultdata', '영어단어.csv')
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)  # 결과 디렉토리가 없으면 생성
    pdf_to_csv(pdf_path, csv_path, start_page=0, end_page=5)  # 예: 첫 5 페이지만 변환
