import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_VALIDATION_API_KEY')
)

def validate_quiz_format(content):
    """
    Validate the format of the generated quiz content by comparing the number of questions and answers.
    """
    print("Executing validate_quiz_format...")
    lines = content.split('\n')
    
    # 공백 라인 제거
    lines = [line.strip() for line in lines if line.strip()]
    
    questions = [line for line in lines if line.lower().startswith("question:")]
    answers = [line for line in lines if line.lower().startswith("answer:")]
    
    # 디버깅 출력 추가
    print(f"Total lines: {len(lines)}")
    print(f"Questions: {len(questions)}")
    print(f"Answers: {len(answers)}")
    print(f"Content: {content}")

    if len(questions) != len(answers) or len(questions) == 0:
        error_message = "Number of questions does not match number of answers or no questions found."
        print("Validation failed:", error_message)
        return [error_message]
    else:
        print("Validation passed: Number of questions matches number of answers.")
        return []

def validate_quiz_content_with_gpt(content):
    """
    Validate the content of the generated quiz using GPT.
    """
    print("Executing validate_quiz_content_with_gpt...")
    prompt = ("Please review the following quiz content for accuracy and quality. "
              "If there are any errors or issues, provide detailed feedback. "
              "If the content is good, simply state 'Content is good'.\n\n"
              "Quiz Content:\n" + content)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a validator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0
        )
        print("Response from GPT:", response)  # 응답 구조 확인
        feedback = response.choices[0].message.content.strip()  # 올바른 접근 방식
        print("validate_quiz_content_with_gpt result:", feedback)

        if "Content is good" in feedback:
            return []
        else:
            return [feedback]
    except Exception as e:
        print("Error in validate_quiz_content_with_gpt:", str(e))
        return [str(e)]
    
def validate_subject_knowledge(content, subject):
    """
    Validate the content of the generated educational material for subject-specific knowledge.
    """
    print(f"Executing validate_subject_knowledge for {subject}...")
    prompt = (f"Please review the following educational material for {subject} knowledge. "
              "If there are any inaccuracies or issues, provide detailed feedback. "
              "If the content is accurate, simply state 'Content is accurate'.\n\n"
              f"{subject} Content:\n" + content)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a {subject} expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0
        )
        feedback = response.choices[0].message.content.strip()
        print(f"validate_subject_knowledge result for {subject}:", feedback)

        if "Content is accurate" in feedback:
            return []
        else:
            return [feedback]
    except Exception as e:
        print(f"Error in validate_subject_knowledge for {subject}:", str(e))
        return [str(e)]
