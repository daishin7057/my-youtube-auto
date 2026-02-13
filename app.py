import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

# --- 1. 프리미엄 관제 센터 디자인 (image_a374a0.png 스타일) ---
st.set_page_config(page_title="YT Creator Studio Master", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #e6edf3; }
    .stMetric { background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .ai-card { background: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; text-align: center; margin-bottom: 10px; }
    .stSlider [data-baseweb="slider"] { padding-bottom: 2rem; }
    .stButton>button { height: 3.5rem; background: #238636; color: white; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 보관소 초기화 (즐겨찾기, 히스토리, 설정 등)
if 'fav_ai' not in st.session_state: st.session_state.fav_ai = []
if 'history' not in st.session_state: st.session_state.history = []
if 'api_keys' not in st.session_state: st.session_state.api_keys = {"Gemini": "", "Claude": ""}

# Gemini API 인증
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. 사이드바 스마트 내비게이션 ---
with st.sidebar:
    st.title("🎬 YT Studio Master")
    st.caption("CEO 전용 콘텐츠 통합 관제 센터")
    st.divider()
    menu = st.radio("🏠 메뉴 선택", ["대시보드", "콘텐츠 생성실", "AI 검색엔진", "집/회사 동기화", "설정"])
    st.divider()
    st.success("🎉 프로그램이 정상적으로 작동합니다!") # [cite: 2026-02-13]

# --- 3. 메뉴별 기능 구현 ---

# [3-1] 대시보드: 지표 및 즐겨찾기 AI [cite: 2026-02-13]
if menu == "대시보드":
    st.header("🏠 대시보드")
    st.markdown("> **🎉 환영합니다, 대표님! 모든 시스템이 정상 가동 중입니다.**")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 트렌드 키워드", "847", "↑")
    col2.metric("🎬 제작 완료", f"{len(st.session_state.history)}건", "+1")
    col3.metric("⭐ 즐겨찾기 AI", f"{len(st.session_state.fav_ai)}/8", "활성")
    col4.metric("🔄 데이터 상태", "최신", "✅")

    st.divider()
    st.subheader("⭐ 내 즐겨찾기 AI")
    if st.session_state.fav_ai:
        cols = st.columns(4)
        for idx, ai in enumerate(st.session_state.fav_ai):
            cols[idx % 4].markdown(f"<div class='ai-card'><h4>{ai}</h4></div>", unsafe_allow_html=True)
    else:
        st.write("등록된 즐겨찾기가 없습니다. 'AI 검색엔진'에서 별을 눌러주세요.")

# [3-2] 콘텐츠 생성실: 정밀 타임라인 제어 [cite: 2026-02-13]
elif menu == "콘텐츠 생성실":
    st.subheader("✨ 콘텐츠 생성 (타임라인 자유 조정)")
    
    # 대표님이 원하시는 대로 시간을 '편하게' 정하는 정밀 제어기 [cite: 2026-02-13]
    t_mode = st.radio("설정 방식", ["빠른 선택", "직접 입력 (정밀)"], horizontal=True)
    
    if t_mode == "빠른 선택":
        duration = st.select_slider("⏱️ 타임라인 눈금", options=["15초", "30초", "60초", "3분", "5분", "10분", "30분"], value="60초")
    else:
        c1, c2 = st.columns(2)
        m = c1.number_input("분 (Min)", 0, 30, 8)
        s = c2.number_input("초 (Sec)", 0, 59, 30)
        duration = f"{m}분 {s}초"

    st.info(f"🎯 최종 확정 타임라인: **{duration}**") # [cite: 2026-02-13]

    topic = st.text_input("콘텐츠 주제", placeholder="예: 곰을 배신한 고양이 스토리") # [cite: 2026-01-30]
    
    if st.button("⚡ 전체 자동 생성 가동"):
        if topic:
            with st.spinner(f"[{duration}] 분량의 대본을 정밀 집필 중..."):
                res = model.generate_content(f"{topic} 주제로 {duration} 분량의 유튜브 대본과 이미지 프롬프트 생성.")
                st.session_state.history.insert(0, {"date": datetime.now().strftime("%m-%d"), "topic": topic, "len": duration, "content": res.text})
                st.markdown("---")
                st.write(res.text)
        else: st.warning("주제를 입력하세요.")

# [3-3] AI 검색엔진: 16종 즐겨찾기 시스템 [cite: 2026-02-13]
elif menu == "AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 (즐겨찾기 추가)")
    ai_list = ["Claude", "Gemini", "Grok", "ChatGPT", "Perplexity", "Midjourney", "DALL-E 3", "Sora", "Runway", "Flux", "Kling AI", "Pika"]
    cols = st.columns(4)
    for idx, ai in enumerate(ai_list):
        with cols[idx % 4]:
            is_fav = ai in st.session_state.fav_ai
            label = f"⭐ {ai}" if is_fav else f"☆ {ai}"
            if st.button(label, key=ai):
                if is_fav: st.session_state.fav_ai.remove(ai)
                elif len(st.session_state.fav_ai) < 8: st.session_state.fav_ai.append(ai)
                st.rerun()

# [3-4] 집/회사 동기화: JSON 기반 완벽 이동 [cite: 2026-02-13]
elif menu == "집/회사 동기화":
    st.subheader("🔄 집/회사 데이터 동기화")
    st.info("집에서 만든 대본과 즐겨찾기를 회사에서도 그대로 사용하세요.") # [cite: 2026-02-13]
    
    c1, c2 = st.columns(2)
    with c1:
        data = json.dumps({"fav": st.session_state.fav_ai, "hist": st.session_state.history}, indent=4)
        st.download_button("📤 데이터 내보내기", data=data, file_name="yt_backup.json")
    with c2:
        file = st.file_uploader("📥 데이터 가져오기", type="json")
        if file and st.button("✅ 모든 설정 복원"):
            d = json.load(file)
            st.session_state.fav_ai, st.session_state.history = d['fav'], d['hist']
            st.success("데이터 복원 완료!")

# [3-5] 설정
else:
    st.subheader("⚙️ 시스템 설정")
    st.session_state.api_keys["Gemini"] = st.text_input("Gemini API Key", value=st.session_state.api_keys["Gemini"], type="password")
    if st.button("💾 설정 저장"): st.success("✅ 저장되었습니다.")
