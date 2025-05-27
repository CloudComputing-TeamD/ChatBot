from fastapi import FastAPI
from pydantic import BaseModel
from gpt_intent import classify_intent_gpt
from llm_answer import answer_question
import requests

app = FastAPI()

# 요청 body 정의
class MessageRequest(BaseModel):
    message: str



@app.post("/chat")
async def chat_endpoint(data: MessageRequest):
    user_input = data.message
    parsed = classify_intent_gpt(user_input)  # {"intent": "...", "category": "하체" 등}

    if parsed["intent"] == "routine":
        # 루틴 요청 JSON 생성
        routine_req_payload = {
            "level": parsed.get("level", "beginner"),
            "goal": parsed.get("goal", "fat_loss"),
            "preferred_parts": parsed["preferred_parts"],
            "frequency_per_week": parsed.get("frequency_per_week", 1),
            "top_k": parsed.get("top_k", 3),
        }

        try:
            return routine_req_payload
            # 루틴 서버에 POST 요청

            #response = requests.post("http://routine-server.example.com/routine", json=routine_req_payload)
            #response.raise_for_status()
            #routine = response.json()

            # 전체 Day 추출 및 정리
            # days = []
            # for day_key in sorted(routine_response.keys()):
            #     day_data = routine_response[day_key]
            #     days.append({
            #         "day": day_key,
            #         "target_parts": day_data.get("target_parts", []),
            #         "exercises": day_data.get("exercises", [])
            #     })
            # 최종 응답
            # return {
            #     "type": "routine",
            #     "preferred_parts": preferred_parts,
            #     "level": routine_req_payload["level"],
            #     "goal": routine_req_payload["goal"],
            #     "frequency_per_week": routine_req_payload["frequency_per_week"],
            #     "routine": days
            # }

        except requests.RequestException as e:
            return {
                "type": "error",
                "message": "루틴 추천 서버 요청에 실패했습니다.",
                "details": str(e)
            }

    elif parsed["intent"] == "qa":
        answer = answer_question(user_input)
        return {
            "type": "qa",
            "question": user_input,
            "answer": answer
        }

    else:
        return {
            "type": "error",
            "message": "의도를 분류하지 못했습니다."
        }
