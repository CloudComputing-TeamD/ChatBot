from openai import OpenAI
import json
from open_api_key import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_json_from_gpt(content: str):
    json_start = content.find("{")
    json_end = content.rfind("}") + 1
    json_str = content[json_start:json_end]
    return json.loads(json_str)

def classify_intent_gpt(user_input):
    system_prompt = """
당신은 사용자의 문장을 분석하여 운동 루틴 추천 요청인지 일반 질문인지를 구분하고,  
운동 루틴 추천 요청일 경우 아래의 JSON 형식으로 정보를 추출합니다.
단순 운동 추천 요청도 루틴 추천 요청으로 판단합니다.

### 운동 루틴 추천 요청이면 다음과 같은 JSON을 생성하세요:

{
  "intent": "routine",
  "goal": "운동 목표",                     // 가능한 값: muscle_gain, fat_loss, maintenance
  "preferred_parts": [운동 부위 리스트],    // 가능한 값: CHEST, BACK, LEGS, SHOULDERS, ARMS, CORE, FULL_BODY
  "level": "운동 난이도",                  // 가능한 값: beginner, intermediate, advanced
  "gender": "성별",                        // 가능한 값: male, female, 요청에 대한 적절한 입력값이 없으면 Null.
  "weight": 체중,                        // 가능한 값: int값, 요청에 대한 적절한 입력값이 없으면 Null.
  "top_k": 운동 부위별 운동 개수            // 가능한 값: 1부터 5까지. 기본값은 5.
}

예시:
입력: "초보자고 뱃살 빼고 싶어요. 하체랑 복부 운동 추천해줘"
출력:
{
  "intent": "routine",
  "goal": "fat_loss",
  "preferred_parts": ["LEGS", "CORE"],
  "level": "beginner",
  "gender": null,
  "weight" : null,
  "top_k": 5
}

예시:
입력: "여자인데 꾸준히 운동을 하고있습니다. 등 근육을 키우고 싶은데 체중은 50키로 입니다."
{
  "intent": "routine",
  "goal": "muscle_gain",
  "preferred_parts": ["BACK"],
  "level": "intermediate",
  "gender": "female",
  "weight" : 50,
  "top_k": 5
}

---

### 운동에 대한 일반 질문일 경우는 아래와 같이 작성하세요:

{
  "intent": "qa",
  "preferred_parts": null,
  "level": null,
  "gender": null,
  "goal": null,
  "top_k": null
}

예시:
입력: "스쿼트는 어디에 좋은 운동인가요?"
출력:
{
  "intent": "qa",
  "preferred_parts": null,
  "level": null,
  "gender": null,
  "goal": null,
  "top_k": null
}

---
반드시 JSON 형식으로만 출력하고, 설명이나 주석은 절대 쓰지 마세요.
중괄호 `{}`로 시작해서 끝나는 JSON 하나만 출력하세요.

"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.2,
            max_tokens=100
        )

        content = response.choices[0].message.content
        result = extract_json_from_gpt(content)
        return result
    except Exception as e:
        print("[GPT ERROR]", e)
        return {
            "intent": "qa",
            "preferred_parts": None,
            "level": None,
            "gender": None,
            "goal": None,
            "top_k": None
        }

