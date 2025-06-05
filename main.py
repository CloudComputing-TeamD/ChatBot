from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from gpt_intent import classify_intent_gpt
from llm_answer import answer_question
import requests

app = FastAPI()

# 요청 body 정의
class UserData(BaseModel):
    goal: Optional[str] = "fat_loss"
    preferred_parts: Optional[List[str]] = []
    level: Optional[str] = "beginner"
    gender: Optional[str] = None
    weight: Optional[float] = None
    top_k: Optional[int] = 5


class MessageRequest(BaseModel):
    message: str
    userData: Optional[UserData] = None



@app.post("/chat")
async def chat_endpoint(data: MessageRequest):
    user_input = data.message
    user_data = data.userData
    parsed = classify_intent_gpt(user_input)  # {"intent": "...", "category": "하체" 등}

    
    if parsed["intent"] == "routine":
        # 루틴 요청 JSON 생성
        routine_req_payload = {
            "goal": parsed.get("goal") if parsed.get("goal") is not None else user_data.goal,
            "preferred_parts": parsed.get("preferred_parts") if parsed.get("preferred_parts") else user_data.preferred_parts,
            "level": parsed.get("level") if parsed.get("level") is not None else user_data.level,
            "gender": parsed.get("gender") if parsed.get("gender") is not None else user_data.gender,
            "weight": parsed.get("weight") if parsed.get("weight") is not None else user_data.weight,
            "top_k": parsed.get("top_k") if parsed.get("top_k") is not None else user_data.top_k,
        }

        try:
            #return routine_req_payload
            # 루틴 서버에 POST 요청

            response = requests.post("http://34.227.127.99/recommend", json=routine_req_payload)
            response.raise_for_status()
            routine = response.json()

            #return routine
            # 최종 응답
            return {
                "type": "routine",
                "preferred": routine_req_payload["preferred_parts"],
                "level": routine_req_payload["level"],
                "goal": routine_req_payload["goal"],
                "routine": {
                    "name": routine.get("name"),
                    "routineItems": routine.get("routineItems")
                }
            }

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
