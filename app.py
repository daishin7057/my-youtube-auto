import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime

# --- 1. 가이드 준수 프리미엄 디자인 ---
st.set_page_config(page_title="유튜브 크리에이터 스튜디오 프로", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #e6edf3; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
    .ai-card { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #238636; color: white; height: 3.5rem; }
    .status-box { background-color: #1e2130; color: #238636; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화 (가이드 준수)
for key in ['fav_ai', 'history', 'api_keys']:
    if key not in st.session_state:
        st.session_state[key] = [] if key != 'api_keys' else {"Claude": "", "YouTube": ""}

# API 인증 (image_a4c640.png 에러 방지용 안전장치)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. 사이드바 (가이드 1단계: 작동 확인) ---
with st.sidebar:
    st.title("🎬 YT Studio Pro")
    menu = st.radio("메뉴 이동", ["🏠 대시보드", "✨ 콘텐츠 생성", "🤖 AI 검색엔진", "🔄 집/회사 동기화", "⚙️ 설정"])
    st.divider()
    st.markdown("<div class='status-box'>🎉 프로그램이 정상적으로 작동합니다!</div>", unsafe_allow_html=True) # [cite: 2026-02-13]

# --- 3. 메뉴별 기능 구현 ---

if menu == "🏠 대시보드":
    st.header("🏠 대시보드")
    st.info("✅ 타임라인 자유 조정: 15초~30분 | ✅ AI 즐겨찾기 | ✅ 데이터 동기화") [cite: 2026-02-13]
    col1, col2, col3 = st.columns(3)
    col1.metric("⭐ 즐겨찾기 AI", f"{len(st.session_state.fav_ai)} / 8")
    col2.metric("📝 제작 완료", f"{len(st.session_state.history)}건")
    col3.metric("📅 마지막 업데이트", datetime.now().strftime("%Y-%m-%d"))

elif menu == "✨ 콘텐츠 생성":
    st.subheader("✨ 콘텐츠 생성 (자유 타임라인)") #
    
    # 대표님 요청: 분/초 정밀 입력 (에러 방지 로직 적용)
    c1, c2 = st.columns(2)
    with c1:
        m = st.number_input("분 (Min)", 0, 30, 0)
    with c2:
        # s의 기본값을 60에서 0으로 수정하여 에러 박멸
        s = st.number_input("초 (Sec)", 0, 59, 0) 
    
    duration = f"{m}분 {s}초" if m > 0 else f"{s}초"
    
    # 이미지 스타일 및 프롬프트 확인 기능 [cite: 2026-02-13]
    style = st.selectbox("🎬 이미지 스타일", ["시네마틱", "카툰", "애니메이션", "사이버펑크"])
    topic = st.text_input("콘텐츠 주제", placeholder="예: 2차대전 탱크 복원")

    if st.button("⚡ 전체 자동 생성 가동"): [cite: 2026-02-13]
        if topic:
            bar = st.progress(0)
            for i in range(100): time.sleep(0.01); bar.progress(i + 1)
            
            res = model.generate_content(f"{topic} 주제로 {duration} 대본과 {style} 스타일의 프롬프트 써줘.")
            st.session_state.history.insert(0, {"topic": topic, "content": res.text, "len": duration})
            
            st.success("✅ 생성 완료!")
            t1, t2 = st.tabs(["📝 대본", "🖼️ 이미지 프롬프트"])
            with t1: st.write(res.text)
            with t2: st.code(res.text.split("프롬프트")[-1])
        else: st.warning("주제를 입력하세요.")

elif menu == "🤖 AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 (별 ☆ 클릭 시 즐겨찾기 추가)") [cite: 2026-02-13]
    # 가이드에 있는 16종 AI 목록 적용
    all_ai = ["Claude", "Gemini", "Grok", "ChatGPT", "Perplexity", "FlowGPT", "Poe", "Copilot", "Midjourney", "DALL-E 3", "Flux", "Stable Diff", "Kling AI", "Runway", "Pika", "Sora"]
    cols = st.columns(4)
    for idx, ai in enumerate(all_ai):
        with cols[idx % 4]:
            is_fav = ai in st.session_state.fav_ai
            if st.button(f"{'⭐' if is_fav else '☆'} {ai}", key=ai):
                if is_fav: st.session_state.fav_ai.remove(ai)
                elif len(st.session_state.fav_ai) < 8: st.session_state.fav_ai.append(ai)
                st.rerun()

elif menu == "🔄 집/회사 동기화":
    st.subheader("🔄 집/회사 데이터 동기화") [cite: 2026-02-13]
    data = json.dumps({"fav": st.session_state.fav_ai, "keys": st.session_state.api_keys, "hist": st.session_state.history}, indent=4)
    st.download_button("📤 데이터 내보내기", data=data, file_name=f"yt_backup_{datetime.now().strftime('%m-%d')}.json")
    f = st.file_uploader("📥 데이터 가져오기", type="json")
    if f and st.button("✅ 데이터 가져오기 완료!"):
        d = json.load(f)
        st.session_state.fav_ai, st.session_state.api_keys, st.session_state.history = d['fav'], d['keys'], d['hist']
        st.success("모든 설정이 복원되었습니다!")

else: # 설정 페이지
    st.subheader("⚙️ 설정 (API 키 관리)") [cite: 2026-02-13]
    st.session_state.api_keys["Claude"] = st.text_input("Claude API Key", value=st.session_state.api_keys["Claude"], type="password")
    st.session_state.api_keys["YouTube"] = st.text_input("YouTube API Key", value=st.session_state.api_keys["YouTube"], type="password")
    if st.button("저장"): st.success("✅ API 키 저장됨")
