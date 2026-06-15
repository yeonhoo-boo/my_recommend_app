from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline 

app = FastAPI()

# 수업 자료에 나온 Hugging Face 감정 분석 파이프라인 활용 
classifier = pipeline("sentiment-analysis") 

class UserInput(BaseModel):
    text: str
    interest: str

@app.post("/recommend")
def get_recommendation(data: UserInput):
    # 1. Hugging Face AI 모델로 사용자의 현재 상태/문장 분석 
    analysis = classifier(data.text)[0] 
    status = analysis['label']  # 'POSITIVE' 또는 'NEGATIVE' 
    
    # 2. 전공 성향과 상태에 따른 맞춤형 추천 로직 (개인 차별성 확보)
    interest_area = data.interest
    
    if interest_area == "인공지능/데이터":
        if status == "POSITIVE":
            rec_course = "딥러닝 실습 및 오픈소스 소프트웨어 고급 과정"
            advice = "열정이 넘치시네요! 대규모 파이프라인을 다루는 프로젝트를 추천합니다."
        else:
            rec_course = "기초 데이터 분석 및 선형대수학 개념 다지기"
            advice = "조금 지치셨을 수 있습니다. 기초부터 차근차근 다지는 세션을 추천해요."
            
    elif interest_area == "웹/앱 개발":
        if status == "POSITIVE":
            rec_course = "FastAPI + Streamlit을 활용한 풀스택 아키텍처"
            advice = "현재 컨디션이 좋습니다. Docker 복합 컨테이너 빌드에 도전해보세요!"
        else:
            rec_course = "UI/UX 디자인 및 웹 퍼블리싱 기초"
            advice = "복잡한 백엔드 로직보다는 가벼운 프론트엔드 화면 구현부터 시작해봅시다."
            
    else:
        rec_course = "컴퓨터 공학 개론 및 프로그래밍 입문"
        advice = "새로운 분야 탐색을 위해 넓고 얕은 지식부터 습득하는 것을 추천합니다."

    return {
        "ai_status": "긍정적" if status == "POSITIVE" else "불안정/지침",
        "recommended_course": rec_course,
        "custom_advice": advice
    }