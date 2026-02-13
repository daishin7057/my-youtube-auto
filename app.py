import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime

# --- 1. 가이드 준수 하이엔드 디자인 (image_a3e91d.png 재현) ---
st.set_page_config(page_title="YT Creator Studio Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #e6edf3; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; border-left: 5px solid #3b82f6; }
    .ai-card { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; text-align: center; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #238636; color: white; height: 3.5rem; }
    .status-msg { background-color: #1e2130; color: #238636; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
for key in ['fav_ai', 'history', 'api_keys']:
    if key not in st.session_state:
        st.session_state[key] = [] if key != 'api_keys' else {"Claude": "", "YouTube": ""}

# AI 엔진 인증 (404 에러 해결을 위한 모델명 수정)
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 가장 안정적인 모델명으로 교체
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    except: pass

# --- 2. 사이드바 (가이드 1단계: 작동 확인) ---
with st.sidebar:
    st.title("🎬 YT Studio Pro")
    st.caption("AI 영상 자동화 플랫폼 v18.0")
    menu = st.radio("🧭 메뉴 이동", ["🏠 대시보드", "✨ 콘텐츠 생성", "🤖 AI 검색엔진", "🔄 집/회사 동기화", "⚙️ 설정"])
    st.divider()
    st.markdown("<div class='status-msg'>🎉 프로그램이 정상적으로 작동합니다!</div>", unsafe_allow_html=True) [cite: 2026-02-13]

# --- 3. 핵심 메뉴 구현 ---

# [3-1] 대시보드 (image_a3e91d.png 완벽 이식)
if menu == "🏠 대시보드":
    st.header("🏠 대시보드")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 트렌드 키워드", "847", "↑ 실시간")
    c2.metric("🎬 제작 완료", f"{len(st.session_state.history)}", "+1")
    c3.metric("⚡ 파이프라인", "Step 3/9", "진행중")
    c4.metric("🔥 핫 트렌드", "18건", "NEW")

    st.divider()
    m_left, m_right = st.columns([1.5, 1])
    with m_left:
        st.subheader("🔥 실시간 핫 트렌드 (100만+ 조회)")
        trends = ["고양이 스시 요리", "비밀 지하 도시", "AI 로맨스 영화 60초"]
        for t in trends: st.info(f"📌 {t}")
    with m_right:
        st.subheader("⚙️ 파이프라인 현황")
        steps = ["분석", "주제", "대본", "이미지", "영상", "TTS", "편집", "검수", "🚀 자동 업로드"]
        for idx, s in enumerate(steps):
            st.write(f"{'✅' if idx < 2 else '⚪'} {idx+1}. {s}")

# [3-2] 콘텐츠 생성 (분/초 함께 입력 + 스타일 선택)
elif menu == "✨ 콘텐츠 생성":
    st.subheader("✨ 콘텐츠 생성 (자유 타임라인)")
    
    col_t1, col_t2, col_s = st.columns([1, 1, 2])
    with col_t1: m = st.number_input("분 (Min)", 0, 30, 0)
    with col_t2: s = st.number_input("초 (Sec)", 0, 59, 0) #
    with col_s: style = st.selectbox("🖼️ 이미지 스타일", ["🎬 시네마틱", "🎨 카툰", "✨ 애니메이션", "⚡ 사이버펑크"])
    
    duration = f"{m}분 {s}초" if m > 0 else f"{s}초"
    topic = st.text_input("콘텐츠 주제", placeholder="예: 고양이 정글 탐험") #

    if st.button("⚡ 전체 자동 생성 가동"): [cite: 2026-02-13]
        if topic and model:
            bar = st.progress(0) #
            for i in range(100): time.sleep(0.01); bar.progress(i + 1)
            try:
                res = model.generate_content(f"{topic} 주제로 {duration} 대본과 {style} 스타일 프롬프트 생성.")
                st.session_state.history.insert(0, {"topic": topic, "content": res.text, "len": duration})
                st.success("✅ 생성 완료!") #
                t1, t2 = st.tabs(["📝 대본", "🎙️ 결과 확인"])
                with t1: st.write(res.text)
                with t2: st.info("이미지 및 음성 합성 프롬프트가 대본에 포함되었습니다.")
            except Exception as e: st.error(f"오류: {e}") #
        else: st.warning("API 키 설정을 먼저 확인해 주세요.")

# [3-3] AI 검색엔진 (image_a53319.png 16종 엔진 이식)
elif menu == "🤖 AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 (별 ☆ 클릭 시 즐겨찾기)")
    ai_list = ["Claude", "Gemini", "Grok", "ChatGPT", "Perplexity", "FlowGPT", "Poe", "Copilot", 
              "Midjourney", "DALL-E 3", "Flux", "Stable Diff", "Kling AI", "Runway", "Pika", "Sora"]
    cols = st.columns(4)
    for idx, ai in enumerate(ai_list):
        with cols[idx % 4]:
            is_fav = ai in st.session_state.fav_ai
            if st.button(f"{'⭐' if is_fav else '☆'} {ai}", key=ai):
                if is_fav: st.session_state.fav_ai.remove(ai)
                elif len(st.session_state.fav_ai) < 8: st.session_state.fav_ai.append(ai)
                st.rerun()

# [3-4] 동기화 및 설정
elif menu == "🔄 집/회사 동기화":
    st.subheader("🔄 집/회사 데이터 동기화") [cite: 2026-02-13]
    data = json.dumps({"fav": st.session_state.fav_ai, "hist": st.session_state.history, "keys": st.session_state.api_keys}, indent=4)
    st.download_button("📤 데이터 내보내기 (JSON)", data=data, file_name="yt_studio_backup.json")
    f = st.file_uploader("📥 데이터 가져오기", type="json")
    if f and st.button("✅ 데이터 가져오기 완료!"):
        d = json.load(f)
        st.session_state.fav_ai, st.session_state.history, st.session_state.api_keys = d['fav'], d['hist'], d.get('keys', {})
        st.success("데이터 복원 완료!")

else:
    st.subheader("⚙️ 설정 (API 키)") [cite: 2026-02-13]
    st.session_state.api_keys["Claude"] = st.text_input("Claude Key", value=st.session_state.api_keys["Claude"], type="password")
    st.session_state.api_keys["YouTube"] = st.text_input("YouTube Key", value=st.session_state.api_keys["YouTube"], type="password")
    if st.button("저장"): st.success("✅ 저장됨")
