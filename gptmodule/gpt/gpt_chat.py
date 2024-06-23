from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def gpt_chat(prompt, age_category, grade_category, subject_category, request_type, language_setting):
    print("Executing gpt_chat...")
    print(f"Prompt: {prompt}, Age Category: {age_category}, Grade Category: {grade_category}, Subject Category: {subject_category}, Request Type: {request_type}, Language Setting: {language_setting}")

    # 시스템 메시지 설정
    if language_setting == "한국어":
        if age_category == "student":
            system_message = f"당신은 {grade_category} {subject_category} 과목을 가르치는 선생님입니다. 학생 수준에 맞춰서 설명해 주세요. 폭력적이거나 혐오적인 표현을 사용하지 마세요."
        else:
            system_message = f"당신은 성인을 위한 {subject_category} 과목을 가르치는 선생님입니다. 폭력적이거나 혐오적인 표현을 사용하지 마세요."
    else:
        if age_category == "student":
            system_message = f"You are a teacher for {grade_category} level {subject_category} subject. Please explain at the student's level. Do not use violent or hateful language."
        else:
            system_message = f"You are a teacher for adults learning {subject_category} subject. Do not use violent or hateful language."

    print(f"System message: {system_message}")

    # GPT-3.5 API 호출
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content.strip()
        print("gpt_chat result:", result)
        return result
    except Exception as e:
        print(f"Error in gpt_chat: {str(e)}")
        raise