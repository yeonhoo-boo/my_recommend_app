import streamlit as st
import requests

st.set_page_config(page_title="AI 맞춤 과목 추천 시스템", layout="centered")

st.title("🎓 AI 기반 전공 과목 및 학습 전략 추천")
st.write("당신의 현재 마음 상태와 관심 분야를 분석하여 최적의 커리큘럼을 추천합니다.")

# 1. 사용자 입력 받기 (과제 필수 조건)
interest = st.selectbox("관심 있는 핵심 IT 분야를 선택하세요:", ["인공지능/데이터", "웹/앱 개발", "기타 기초"])
user_text = st.text_area("요즘 공부하면서 느끼는 점이나 기분을 솔직하게 적어주세요 (영어 권장):", 
                         placeholder="I am dynamic and ready to learn big models!")

# 2. 추천 요청 버튼
if st.button("AI 맞춤 추천 받기"):
    if user_text.strip() == "":
        st.warning("분석을 위해 문장을 입력해주세요!")
    else:
        with st.spinner("FastAPI 백엔드 엔진에서 AI 분석 중..."):
            try:
                # Docker Compose 환경 내부의 'back' 컨테이너로 HTTP 통신 요청 (과제 필수 조건)
                payload = {"text": user_text, "interest": interest}
                response = requests.post("http://back:8000/recommend", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 3. 응답 결과를 화면에 이쁘게 표시
                    st.success("🎯 분석이 완료되었습니다!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="AI가 분석한 당신의 상태", value=result["ai_status"])
                    with col2:
                        st.text("추천 타겟 과목:")
                        st.code(result["recommended_course"])
                        
                    st.info(f"💡 조언: {result['custom_advice']}")
                else:
                    st.error("백엔드 서버 연동에 실패했습니다.")
            except Exception as e:
                st.error(f"서버 연결 에러 발생: {e}")