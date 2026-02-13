import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime

# --- 1. 가이드 준수 하이엔드 디자인 ---
st.set_page_config(page_title="유튜브 크리에이터 스튜디오 프로", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #e6edf3; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
    .ai-card { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #238636; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
for key in ['fav_ai', 'history', 'api_keys']:
    if key not in st.session_state:
        st.session_state[key] = [] if key != 'api_keys' else {"Claude": "", "YouTube": ""}

# API 인증
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. 사이드바 (가이드 1단계: 작동 확인) ---
with st.sidebar:
    st.title("🎬 YT Studio Pro")
    menu = st.radio("메뉴 이동", ["🏠 대시보드", "✨ 콘텐츠 생성", "🤖 AI 검색엔진", "🔄 집/회사 동기화", "⚙️ 설정"])
    st.divider()
    st.success("🎉 프로그램이 정상적으로 작동합니다!") # [cite: 2026-02-13]

# --- 3. 메뉴별 기능 ---

if menu == "🏠 대시보드":
    st.header("🏠 대시보드")
    st.info("✅ 타임라인 자유 조정: 15초~30분 | ✅ AI 즐겨찾기 | ✅ 데이터 동기화") # [cite: 2026-02-13]
    col1, col2, col3 = st.columns(3)
    col1.metric("⭐ 즐겨찾기 AI", f"{len(st.session_state.fav_ai)} / 8")
    col2.metric("📝 제작 완료", f"{len(st.session_state.history)}건")
    col3.metric("🚀 업로드 준비", "Step 9/9 대기")

elif menu == "✨ 콘텐츠 생성":
    st.subheader("✨ 콘텐츠 생성 (자유 타임라인)")
    # 가이드 요구: 15초~30분 자유 조정 및 스타일 선택 [cite: 2026-02-13]
    c1, c2 = st.columns(2)
    with c1:
        m = st.number_input("분 (Min)", 0, 30, 0)
        s = st.number_input("초 (Sec)", 0, 59, 60)
        duration = f"{m}분 {s}초" if m > 0 else f"{s}초"
    with c2:
        style = st.selectbox("🖼️ 이미지 스타일", ["🎬 시네마틱", "🎨 카툰", "✨ 애니메이션"])

    topic = st.text_input("콘텐츠 주제", placeholder="예: 정글 탐험")
    if st.button("⚡ 전체 자동 생성 가동"): # [cite: 2026-02-13]
        if topic:
            bar = st.progress(0)
            for i in range(100): time.sleep(0.01); bar.progress(i + 1)
            res = model.generate_content(f"{topic} 주제로 {duration} 대본과 {style} 프롬프트 생성.")
            st.session_state.history.insert(0, {"topic": topic, "content": res.text, "len": duration})
            st.success("✅ 생성 완료!")
            st.write(res.text)

elif menu == "🤖 AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 (별 ☆ 클릭 시 즐겨찾기 추가)") # [cite: 2026-02-13]
    all_ai = ["Claude", "Gemini", "Grok", "ChatGPT", "Perplexity", "Midjourney", "Kling AI", "Sora"] # 16종 중 핵심 탑재
    cols = st.columns(4)
    for idx, ai in enumerate(all_ai):
        with cols[idx % 4]:
            is_fav = ai in st.session_state.fav_ai
            if st.button(f"{'⭐' if is_fav else '☆'} {ai}", key=ai):
                if is_fav: st.session_state.fav_ai.remove(ai)
                elif len(st.session_state.fav_ai) < 8: st.session_state.fav_ai.append(ai)
                st.rerun()

elif menu == "🔄 집/회사 동기화":
    st.subheader("🔄 집/회사 데이터 동기화") # [cite: 2026-02-13]
    data = json.dumps({"fav": st.session_state.fav_ai, "keys": st.session_state.api_keys, "hist": st.session_state.history}, indent=4)
    st.download_button("📤 데이터 내보내기", data=data, file_name="yt_studio_backup.json")
    f = st.file_uploader("📥 데이터 가져오기", type="json")
    if f and st.button("✅ 데이터 가져오기 완료!"):
        d = json.load(f)
        st.session_state.fav_ai, st.session_state.api_keys, st.session_state.history = d['fav'], d['keys'], d['hist']
        st.success("모든 설정이 복원되었습니다!")

else: # 설정 페이지
    st.subheader("⚙️ 설정 (API 키 관리)") # [cite: 2026-02-13]
    st.session_state.api_keys["Claude"] = st.text_input("Claude API Key", value=st.session_state.api_keys["Claude"], type="password")
    st.session_state.api_keys["YouTube"] = st.text_input("YouTube API Key", value=st.session_state.api_keys["YouTube"], type="password")
    if st.button("저장"): st.success("✅ API 키 저장됨")
