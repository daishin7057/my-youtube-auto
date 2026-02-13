import streamlit as st
import google.generativeai as genai

# 클라우드 보안 설정(Secrets)에서 키를 가져오는 방식입니다.
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("대표님, 아직 API 키 설정이 되지 않았습니다. (Secrets 설정 필요)")

st.title("🤖 김 비서의 글로벌 유튜브 공장")
topic = st.text_input("쇼츠 주제를 입력하세요", placeholder="예: 배신하는 고양이 스토리")

if st.button("AI 보좌관 가동"):
    if topic:
        with st.spinner("최상의 대본을 작성 중입니다..."):
            response = model.generate_content(f"{topic} 주제로 유튜브 쇼츠 대본 써줘")
            st.success("대본 작성이 완료되었습니다!")
            st.markdown("---")
            st.write(response.text)
    else:
        st.warning("주제를 입력해 주셔야 일을 시작할 수 있습니다.")
