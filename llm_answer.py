import openai
from open_api_key import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def answer_question(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 운동 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT QA ERROR]: {e}")
        return "gpt 에러 발생"
