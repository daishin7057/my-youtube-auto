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
import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# --- 초기 설정 및 보안 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("대표님, 비밀 금고에 API 키가 없습니다!")

st.set_page_config(page_title="김 비서의 글로벌 유튜브 공장 v3.0", layout="wide")

# --- 데이터 저장소 (Session State) ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 기능 함수: 트렌드 분석 ---
def get_trending_topics():
    # 실제 실시간 API 연결 전, AI 기반 트렌드 예측 로직
    prompt = "최근 3개월 내 유튜브에서 조회수 100만 이상을 기록한 핫한 쇼츠 및 롱폼 주제 5가지를 분석해서 추천해줘."
    res = model.generate_content(prompt)
    return res.text

# --- 사이드바: AI 도구 시트 및 설정 ---
with st.sidebar:
    st.header("📂 공장 관리 데스크")
    menu = st.radio("이동할 구역", ["콘텐츠 제작실", "실시간 트렌드 센터", "AI 도구 백서"])
    
    st.divider()
    st.subheader("🛠️ 제작 설정")
    content_type = st.selectbox("제작 유형", ["숏폼 (Shorts)", "롱폼 (Long-form)"])
    
    if st.button("🔄 트렌드 데이터 갱신"):
        st.session_state.trends = get_trending_topics()

# --- 1구역: AI 도구 백서 (Resource Sheet) ---
if menu == "AI 도구 백서":
    st.title("📚 AI 프로그램 사이트 검색 시트")
    ai_tools = {
        "카테고리": ["언어 모델", "언어 모델", "이미지 생성", "영상 생성", "워크플로우"],
        "프로그램명": ["Gemini", "Claude", "Grok", "Flux / Midjourney", "Flow / LangChain"],
        "주요 용도": ["구글 생태계 연동, 대본", "코딩 및 정교한 글쓰기", "X(트위터) 기반 실시간 정보", "고퀄리티 이미지 제작", "AI 자동화 프로세스 설계"],
        "링크": ["https://gemini.google.com", "https://claude.ai", "https://x.ai", "https://midjourney.com", "https://flowiseai.com"]
    }
    df = pd.DataFrame(ai_tools)
    st.table(df)

# --- 2구역: 실시간 트렌드 센터 ---
elif menu == "실시간 트렌드 센터":
    st.title("🔥 실시간 유튜브 트렌드 분석")
    st.info("최근 3개월 내 조회수 100만 이상의 인기 키워드를 분석합니다.")
    if 'trends' in st.session_state:
        st.markdown(st.session_state.trends)
    else:
        st.write("측면 메뉴의 '트렌드 데이터 갱신' 버튼을 눌러주십시오.")

# --- 3구역: 콘텐츠 제작실 (CRUD 기능 포함) ---
else:
    st.title("🎬 콘텐츠 제작 및 관리")
    
    # 제작 프로세스 확인용 Expander
    with st.expander("🔍 대본이 어떻게 만들어지나요? (프롬프트 구조 보기)"):
        st.code("""
        1. 주제 분석 -> 2. 타겟 맞춤형 톤 설정 -> 3. 후킹 문구 생성 
        -> 4. 장면별 시각 묘사(Image Prompt) 추출 -> 5. 최종 검수
        """)

    # 입력창
    topic = st.text_input("새로운 주제를 입력하세요", placeholder="예: 고양이의 복수")
    
    if st.button("🚀 AI 보좌관 가동"):
        if topic:
            with st.spinner("최상의 대본을 집필 중입니다..."):
                response = model.generate_content(f"{topic} 주제로 {content_type} 대본 써줘")
                new_data = {
                    "id": len(st.session_state.history),
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": content_type,
                    "topic": topic,
                    "content": response.text
                }
                st.session_state.history.insert(0, new_data) # 최신글이 위로

    st.divider()
    
    # 작업 관리자 (Edit / Delete)
    st.subheader("📂 최근 작업 히스토리")
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"[{item['time']}] {item['topic']} ({item['type']})"):
            # 내용 수정
            edited_content = st.text_area("내용 수정", item['content'], key=f"edit_{idx}", height=200)
            if st.button("💾 수정 내용 저장", key=f"save_{idx}"):
                st.session_state.history[idx]['content'] = edited_content
                st.success("수정되었습니다!")
            
            # 삭제 버튼
            if st.button("🗑️ 이 작업 삭제", key=f"del_{idx}"):
                st.session_state.history.pop(idx)
                st.rerun()

            st.markdown("---")
            st.write(item['content'])
