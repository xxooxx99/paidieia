import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def gpt_chat(prompt, language):
    print("Executing gpt_chat...")
    if language == "korean":
        system_message = "당신은 한국어로 답변하는 선생님입니다."
    else:
        system_message = "You are an English teacher."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    result = response.choices[0].message.content
    print("gpt_chat result:", result)
    return result
