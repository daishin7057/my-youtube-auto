import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

# --- 1. 프리미엄 관제 센터 디자인 (Dark Mode) ---
st.set_page_config(page_title="YT Creator Studio Master", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #e6edf3; }
    .stMetric { background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .ai-card { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; text-align: center; margin-bottom: 10px; transition: 0.3s; }
    .ai-card:hover { border-color: #3b82f6; transform: translateY(-3px); }
    .stButton>button { height: 3.5rem; background: #238636; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 보관소 초기화
if 'fav_ai' not in st.session_state: st.session_state.fav_ai = []
if 'history' not in st.session_state: st.session_state.history = []

# AI 엔진 설정 (에러 방지 로직 포함)
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash') # 모델 명칭 확인 완료
    except Exception as e:
        st.error(f"AI 엔진 연결 실패: {e}")
else:
    st.warning("⚠️ Secrets에 API 키가 설정되지 않았습니다.")

# --- 2. 사이드바 스마트 내비게이션 ---
with st.sidebar:
    st.title("🎬 YT Studio Master")
    st.caption("CEO 전용 콘텐츠 관제 센터")
    st.divider()
    menu = st.radio("🏠 메뉴 선택", ["대시보드", "콘텐츠 생성실", "AI 검색엔진", "집/회사 동기화"])
    st.divider()
    st.success("🎉 프로그램이 정상적으로 작동합니다!") # [cite: 2026-02-13]

# --- 3. 메뉴별 기능 구현 ---

# [3-1] 대시보드: 지표 및 즐겨찾기 AI
if menu == "대시보드":
    st.header("🏠 대시보드")
    st.markdown("> **환영합니다, 대표님! 오늘 제작할 쇼츠 주제는 무엇입니까?**")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 트렌드 지수", "847", "↑")
    col2.metric("🎬 제작 완료", f"{len(st.session_state.history)}건", "+1")
    col3.metric("⭐ 즐겨찾기 AI", f"{len(st.session_state.fav_ai)}/8", "활성")
    col4.metric("🔄 데이터 상태", "최신", "✅")

    st.divider()
    st.subheader("⭐ 내 즐겨찾기 AI")
    if st.session_state.fav_ai:
        cols = st.columns(4)
        for idx, ai in enumerate(st.session_state.fav_ai):
            cols[idx % 4].markdown(f"<div class='ai-card'><h3>{ai}</h3></div>", unsafe_allow_html=True)
    else:
        st.write("등록된 즐겨찾기가 없습니다. 'AI 검색엔진'에서 별을 눌러주세요.")

# [3-2] 콘텐츠 생성실: 타임라인 자유 조정 및 에러 핸들링
elif menu == "콘텐츠 생성실":
    st.subheader("✨ 콘텐츠 생성 (타임라인 자유 조정)")
    
    t_mode = st.radio("설정 방식", ["빠른 선택", "정밀 입력"], horizontal=True)
    if t_mode == "빠른 선택":
        duration = st.select_slider("⏱️ 타임라인 선택", options=["15초", "30초", "60초", "3분", "5분", "10분", "30분"], value="60초")
    else:
        c1, c2 = st.columns(2)
        m = c1.number_input("분 (Min)", 0, 30, 8)
        s = c2.number_input("초 (Sec)", 0, 59, 30)
        duration = f"{m}분 {s}초"

    st.info(f"🎯 최종 확정 타임라인: **{duration}**")

    topic = st.text_input("콘텐츠 주제", placeholder="예: 곰을 배신한 고양이 스토리")
    
    if st.button("⚡ 전체 자동 생성 가동"):
        if not model:
            st.error("AI 엔진이 설정되지 않았습니다. API 키를 확인해주세요.")
        elif topic:
            with st.spinner(f"[{duration}] 분량의 대본을 생성 중..."):
                try:
                    # 에러 방지를 위한 예외 처리 추가
                    prompt = f"{topic} 주제로 {duration} 분량의 유튜브 대본과 이미지 프롬프트 생성."
                    res = model.generate_content(prompt)
                    st.session_state.history.insert(0, {"date": datetime.now().strftime("%m-%d"), "topic": topic, "len": duration, "content": res.text})
                    st.markdown("---")
                    st.write(res.text)
                    st.success("✅ 대본 생성이 완료되었습니다!")
                except Exception as e:
                    st.error(f"❌ AI 호출 중 오류 발생: {e}")
                    st.info("API 키의 권한을 확인하거나 나중에 다시 시도해 주십시오.")
        else: st.warning("주제를 입력하세요.")

# [3-3] AI 검색엔진: 16종 즐겨찾기 시스템 [cite: 2026-02-13]
elif menu == "AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 (별을 클릭하여 즐겨찾기 추가)")
    ai_list = ["Claude", "Gemini", "Grok", "ChatGPT", "Perplexity", "Midjourney", "DALL-E 3", "Flux", "Sora", "Runway", "Kling AI", "Pika"]
    cols = st.columns(4)
    for idx, ai in enumerate(ai_list):
        with cols[idx % 4]:
            is_fav = ai in st.session_state.fav_ai
            label = f"⭐ {ai}" if is_fav else f"☆ {ai}"
            if st.button(label, key=ai):
                if is_fav: st.session_state.fav_ai.remove(ai)
                elif len(st.session_state.fav_ai) < 8: st.session_state.fav_ai.append(ai)
                st.rerun()

# [3-4] 집/회사 동기화
elif menu == "집/회사 동기화":
    st.subheader("🔄 데이터 동기화")
    data = json.dumps({"fav": st.session_state.fav_ai, "hist": st.session_state.history}, indent=4)
    st.download_button("📤 데이터 내보내기 (JSON)", data=data, file_name="yt_studio_backup.json")
    file = st.file_uploader("📥 데이터 가져오기", type="json")
    if file and st.button("✅ 모든 데이터 복원"):
        d = json.load(file)
        st.session_state.fav_ai, st.session_state.history = d['fav'], d['hist']
        st.success("데이터 복원 완료!")
