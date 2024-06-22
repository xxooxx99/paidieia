import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def gpt_edit(content):
    print("Executing gpt_edit...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a text editor."},
            {"role": "user", "content": "Check for simple procedural errors and correctness:\n\n" + content}
        ],
        max_tokens=150
    )
    result = response.choices[0].message.content.strip()  
    print("gpt_edit result:", result)
    return result