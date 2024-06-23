import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def gpt_finetune(training_file_id):
    print("Executing gpt_finetune...")
    response = client.fine_tunes.create(
        training_file=training_file_id
    )
    print("gpt_finetune result:", response)
    return response
