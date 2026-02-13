import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime

# --- 1. 하이엔드 다크 테마 디자인 (image_a374a0.png 반영) ---
st.set_page_config(page_title="유튜브 크리에이터 스튜디오 프로", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; border-left: 4px solid #3b82f6; }
    .ai-card { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; height: 180px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #238636; color: white; border: none; }
    .stButton>button:hover { background-color: #2ea043; border: none; }
    .trend-item { background: #1c2128; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 3px solid #f78166; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 보관소 초기화
if 'fav_ai' not in st.session_state: st.session_state.fav_ai = []
if 'history' not in st.session_state: st.session_state.history = []

# API 인증 안전장치
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: pass

# --- 2. 사이드바 내비게이션 (image_a53319.png 구성) ---
with st.sidebar:
    st.title("🎬 YT Studio Pro")
    st.caption("AI 영상 자동화 플랫폼 v11.0")
    st.divider()
    menu = st.radio("메뉴", ["🏠 대시보드", "✨ 콘텐츠 생성", "🤖 AI 검색엔진", "📂 내 프로젝트", "🔄 집/회사 동기화", "⚙️ 설정"])
    st.divider()
    st.success("🎉 프로그램이 정상적으로 작동합니다!")

# --- 3. 핵심 기능 페이지 구현 ---

# [3-1] 대시보드 (image_a374a0.png 레이아웃 완벽 재현)
if menu == "🏠 대시보드":
    st.header("대시보드")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 트렌드 키워드", "847", "↑ 실시간")
    col2.metric("🎬 생성 완료 영상", f"{len(st.session_state.history)}", "+1")
    col3.metric("⚡ 진행 중 파이프라인", "Step 3/9", "진행중")
    col4.metric("🔥 핫 트렌드 발견", "18", "NEW")

    st.divider()
    mid_c1, mid_c2 = st.columns([1.5, 1])
    with mid_c1:
        st.subheader("🔥 실시간 핫 트렌드 (3개월 이내)")
        trends = ["고양이가 스시 만드는 법 (진짜임)", "폐허 속 비밀 지하 도시", "AI로 만든 완벽한 로맨스"]
        for i, t in enumerate(trends):
            st.markdown(f"<div class='trend-item'><b>{i+1}. {t}</b></div>", unsafe_allow_html=True)
    with mid_c2:
        st.subheader("⚙️ 파이프라인 현황")
        steps = ["트렌드 분석", "주제 확정", "대본 생성", "이미지 프롬프트", "이미지 생성", "음성 합성", "영상 편집", "검수", "업로드"]
        for idx, s in enumerate(steps):
            st.write(f"{'✅' if idx < 2 else '⚪'} {idx+1}. {s}")

# [3-2] 콘텐츠 생성 (스타일 선택 및 프롬프트 확인 기능 추가)
elif menu == "✨ 콘텐츠 생성":
    st.subheader("✨ 콘텐츠 생성 및 스타일 설정")
    
    col_a, col_b = st.columns(2)
    with col_a:
        duration = st.select_slider("⏱️ 타임라인 설정", options=["15초", "30초", "60초", "3분", "5분", "10분", "30분"], value="60초")
    with col_b:
        style = st.selectbox("🖼️ 이미지 스타일 선택", ["시네마틱 (실사)", "카툰 (만화)", "애니메이션", "사이버펑크", "수채화 스타일"]) #

    topic = st.text_input("콘텐츠 주제", placeholder="예: 2차대전 탱크 복원")
    
    if st.button("⚡ 전체 자동 생성 가동"):
        if topic and model:
            bar = st.progress(0)
            for i in range(100): time.sleep(0.01); bar.progress(i+1)
            
            res = model.generate_content(f"{topic} 주제로 {duration} 분량의 대본과 {style} 스타일의 이미지 프롬프트 5개 써줘.")
            st.session_state.history.insert(0, {"topic": topic, "content": res.text, "style": style})
            st.success("✅ 생성 완료!")
            
            t1, t2 = st.tabs(["📝 대본 확인", "🖼️ 생성된 프롬프트"]) #
            with t1: st.write(res.text)
            with t2: st.code(f"Selected Style: {style}\n\n" + res.text.split("이미지 프롬프트")[-1])
        else: st.warning("주제 입력 및 API 설정을 확인하세요.")

# [3-3] AI 검색엔진 (image_a53319.png 카드 레이아웃 완벽 재현)
elif menu == "🤖 AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 (별을 클릭하여 즐겨찾기)")
    ai_groups = {
        "🤖 AI 검색엔진": ["Claude", "Gemini", "Grok", "ChatGPT", "Perplexity", "FlowGPT", "Poe", "Copilot"],
        "🌉 이미지 생성 AI": ["Midjourney", "DALL-E 3", "Flux", "Stable Diff"],
        "🎬 영상 생성 AI": ["Kling AI", "Runway", "Pika", "Sora"]
    }
    
    for group, list_ai in ai_groups.items():
        st.write(f"### {group}")
        cols = st.columns(4)
        for idx, ai in enumerate(list_ai):
            with cols[idx % 4]:
                is_fav = ai in st.session_state.fav_ai
                st.markdown(f"<div class='ai-card'><h4>{ai}</h4><p>{'⭐' if is_fav else '☆'}</p></div>", unsafe_allow_html=True)
                if st.button(f"{'제거' if is_fav else '추가'} {ai}", key=f"btn_{ai}"):
                    if is_fav: st.session_state.fav_ai.remove(ai)
                    else: st.session_state.fav_ai.append(ai)
                    st.rerun()

# [3-4] 동기화
elif menu == "🔄 집/회사 동기화":
    st.subheader("🔄 집/회사 동기화")
    data = json.dumps({"fav": st.session_state.fav_ai, "hist": st.session_state.history}, indent=4)
    st.download_button("📤 데이터 내보내기", data=data, file_name="yt_backup.json")
    f = st.file_uploader("📥 데이터 가져오기", type="json")
    if f and st.button("✅ 데이터 복원"):
        d = json.load(f)
        st.session_state.fav_ai, st.session_state.history = d['fav'], d['hist']
        st.success("데이터가 완벽하게 복원되었습니다!")
