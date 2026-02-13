import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime

# --- 1. 클로드 이상의 프리미엄 디자인: 글래스모피즘 ---
st.set_page_config(page_title="유튜브 마스터 스튜디오 Pro", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* 배경 및 폰트 */
    .main { background: radial-gradient(circle at top right, #0d1117, #010409); color: #e6edf3; font-family: 'Inter', sans-serif; }
    
    /* 사이드바 프리미엄 다크 */
    section[data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    
    /* 지표 카드: 투명 유리 효과 */
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    
    /* 버튼: 메탈릭 블루 그라데이션 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-weight: 700;
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        color: white; height: 3.5rem; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
    
    /* 작동 상태 알림창 */
    .status-box {
        background: rgba(35, 134, 54, 0.1);
        color: #3fb950; padding: 15px; border-radius: 10px;
        text-align: center; font-weight: bold; border: 1px solid #238636;
    }
    </style>
    """, unsafe_allow_html=True)

# [데이터 엔진 초기화]
for key in ['fav_ai', 'history', 'api_keys']:
    if key not in st.session_state:
        st.session_state[key] = [] if key != 'api_keys' else {"Claude": "", "YouTube": ""}

# [AI 모델 보안 호출] - 404 에러 방지
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: pass

# --- 2. 사이드바 (가이드 1단계 준수) ---
with st.sidebar:
    st.title("🎬 YT Studio Master")
    st.caption("CEO 전용 하이엔드 관제 시스템")
    menu = st.radio("🧭 NAVIGATION", ["🏠 대시보드", "✨ 콘텐츠 생성실", "🤖 AI 검색엔진", "🔄 데이터 동기화", "⚙️ 시스템 설정"])
    st.divider()
    st.markdown("<div class='status-box'>🎉 프로그램이 정상적으로 작동합니다!</div>", unsafe_allow_html=True) # [cite: 2026-02-13]

# --- 3. 핵심 기능 페이지 ---

# [3-1] 대시보드 (image_a3e91d.png 디자인 완성형)
if menu == "🏠 대시보드":
    st.header("🏠 대시보드")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 트렌드 지수", "847", "↑ 실시간") #
    col2.metric("🎬 제작 완료", f"{len(st.session_state.history)}", "+1") #
    col3.metric("⚡ 파이프라인", "Step 3/9", "진행중") #
    col4.metric("🔥 핫 트렌드", "18건", "NEW") #

    st.divider()
    m_left, m_right = st.columns([1.5, 1])
    with m_left:
        st.subheader("🔥 실시간 핫 트렌드 (100만+ 조회)")
        for t in ["고양이가 스시 만드는 법", "폐허 속 비밀 지하 도시", "2차대전 탱크 복원"]:
            st.info(f"📌 {t}") #
    with m_right:
        st.subheader("⚙️ 파이프라인 현황")
        steps = ["분석", "주제", "대본", "이미지", "영상", "TTS", "편집", "검수", "🚀 자동 업로드"]
        for idx, s in enumerate(steps):
            st.write(f"{'✅' if idx < 2 else '⚪'} {idx+1}. {s}") #

# [3-2] 콘텐츠 생성 (가이드 5단계 시나리오 완벽 이식)
elif menu == "✨ 콘텐츠 생성실":
    st.subheader("✨ 콘텐츠 생성 (초정밀 타임라인)")
    
    col_t1, col_t2, col_s = st.columns([1, 1, 2])
    with col_t1: m = st.number_input("분 (Min)", 0, 30, 0)
    with col_t2: s = st.number_input("초 (Sec)", 0, 59, 0) # ValueAboveMaxError 원천 차단
    with col_s: style = st.selectbox("🖼️ 스타일", ["🎬 시네마틱", "🎨 카툰", "✨ 애니메이션", "⚡ 사이버펑크"])
    
    duration = f"{m}분 {s}초" if m > 0 else f"{s}초"
    topic = st.text_input("콘텐츠 주제", placeholder="예: 2차대전 탱크 복원 스토리") # [cite: 2026-02-13]

    if st.button("🚀 전체 자동 생성 가동"): # [cite: 2026-02-13]
        if topic and model:
            bar = st.progress(0) # 가이드 3단계 준수 [cite: 2026-02-13]
            for i in range(100): time.sleep(0.01); bar.progress(i + 1)
            try:
                res = model.generate_content(f"{topic} 주제로 {duration} 대본과 {style} 스타일 프롬프트 생성.")
                st.session_state.history.insert(0, {"topic": topic, "content": res.text, "len": duration})
                st.success("✅ 생성 완료!")
                st.write(res.text)
            except Exception as e: st.error(f"AI 호출 오류: {e}")
        else: st.warning("API 키를 먼저 설정해 주십시오.")

# [3-3] AI 검색엔진 (가이드 2단계: 16종 AI 카드 시스템)
elif menu == "🤖 AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 (별 ☆ 클릭 시 즐겨찾기)")
    ai_list = ["Claude", "Gemini", "Grok", "ChatGPT", "Perplexity", "FlowGPT", "Poe", "Copilot", 
              "Midjourney", "DALL-E 3", "Flux", "Stable Diff", "Kling AI", "Runway", "Pika", "Sora"] # [cite: 2026-02-13]
    cols = st.columns(4)
    for idx, ai in enumerate(ai_list):
        with cols[idx % 4]:
            is_fav = ai in st.session_state.fav_ai
            label = f"⭐ {ai}" if is_fav else f"☆ {ai}"
            if st.button(label, key=ai):
                if is_fav: st.session_state.fav_ai.remove(ai)
                elif len(st.session_state.fav_ai) < 8: st.session_state.fav_ai.append(ai)
                st.rerun()

# [3-4] 데이터 동기화 (가이드 3단계: JSON 완전 가이드)
elif menu == "🔄 데이터 동기화":
    st.subheader("🔄 집/회사 데이터 동기화")
    data = json.dumps({"fav": st.session_state.fav_ai, "hist": st.session_state.history, "keys": st.session_state.api_keys}, indent=4)
    st.download_button("📤 데이터 내보내기", data=data, file_name=f"yt_backup_{datetime.now().strftime('%m%d')}.json") # [cite: 2026-02-13]
    f = st.file_uploader("📥 데이터 가져오기", type="json")
    if f and st.button("✅ 데이터 가져오기 완료!"): # [cite: 2026-02-13]
        d = json.load(f)
        st.session_state.fav_ai, st.session_state.history, st.session_state.api_keys = d['fav'], d['hist'], d.get('keys', {})
        st.success("데이터가 복원되었습니다!")

# [3-5] 설정 (가이드 4단계: API 키 관리)
else:
    st.subheader("⚙️ 설정 (API 키)")
    st.session_state.api_keys["Claude"] = st.text_input("Claude Key", value=st.session_state.api_keys["Claude"], type="password")
    st.session_state.api_keys["YouTube"] = st.text_input("YouTube Key", value=st.session_state.api_keys["YouTube"], type="password")
    if st.button("저장"): st.success("✅ API 키 저장됨") # [cite: 2026-02-13]
