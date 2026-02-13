import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime

# --- 1. 하이엔드 글래스 다크 디자인 (image_b097e2.png 스타일 고정) ---
st.set_page_config(page_title="유튜브 마스터 스튜디오 Pro", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background: #010409; color: #e6edf3; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #30363d; }
    div[data-testid="stMetric"] { background: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; border-left: 5px solid #3b82f6; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 700; background: #238636; color: white; height: 3.5rem; border: none; }
    .status-msg { background: rgba(35, 134, 54, 0.1); color: #3fb950; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; border: 1px solid #238636; }
    </style>
    """, unsafe_allow_html=True)

# [시스템 데이터 초기화]
for key in ['fav_ai', 'history', 'api_keys']:
    if key not in st.session_state:
        st.session_state[key] = [] if key != 'api_keys' else {"Claude": "", "YouTube": ""}

# [AI 엔진 스마트 탐색] - 404 에러 원천 차단 로직
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 현재 사용 가능한 모델 목록을 스스로 검색
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
        model = genai.GenerativeModel(target_model)
    except Exception as e:
        st.sidebar.error(f"API 연결 대기 중...")

# --- 2. 사이드바 (작동 확인 메시지) ---
with st.sidebar:
    st.title("🎬 YT Studio Master")
    menu = st.radio("🧭 NAVIGATION", ["🏠 대시보드", "✨ 콘텐츠 생성실", "🤖 AI 검색엔진", "🔄 데이터 동기화", "⚙️ 시스템 설정"])
    st.divider()
    st.markdown("<div class='status-msg'>🎉 프로그램이 정상적으로 작동합니다!</div>", unsafe_allow_html=True)

# --- 3. 메뉴별 페이지 ---

if menu == "🏠 대시보드":
    st.header("🏠 대시보드")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 트렌드 지수", "847", "↑ 실시간")
    c2.metric("🎬 제작 완료", f"{len(st.session_state.history)}건", "+1")
    c3.metric("⚡ 파이프라인", "Step 3/9", "진행중")
    c4.metric("🔥 핫 트렌드", "18건", "NEW")
    st.divider()
    l_col, r_col = st.columns([1.5, 1])
    with l_col:
        st.subheader("🔥 실시간 핫 트렌드 (100만+ 조회)")
        for t in ["고양이 스시 요리", "비밀 지하 도시", "2차대전 탱크 복원"]: st.info(f"📌 {t}")
    with r_col:
        st.subheader("⚙️ 파이프라인 현황")
        steps = ["분석", "주제", "대본", "이미지", "영상", "TTS", "편집", "검수", "🚀 자동 업로드"]
        for i, s in enumerate(steps): st.write(f"{'✅' if i < 2 else '⚪'} {i+1}. {s}")

elif menu == "✨ 콘텐츠 생성실":
    st.subheader("✨ 콘텐츠 생성 (초정밀 타임라인)")
    c1, c2, col_s = st.columns([1, 1, 2])
    with c1: m = st.number_input("분 (Min)", 0, 30, 0)
    with c2: s = st.number_input("초 (Sec)", 0, 59, 0) # image_a5b2ba.png 에러 수정 완료
    with col_s: style = st.selectbox("🖼️ 스타일", ["🎬 시네마틱", "🎨 카툰", "✨ 애니메이션"])
    
    topic = st.text_input("콘텐츠 주제", placeholder="예: 고양이가 정글 탐험하는 스토리")
    if st.button("🚀 전체 자동 생성 가동"):
        if topic and model:
            bar = st.progress(0)
            for i in range(100): time.sleep(0.01); bar.progress(i + 1)
            try:
                res = model.generate_content(f"{topic} 주제로 대본과 {style} 스타일 프롬프트 생성.")
                st.session_state.history.insert(0, {"topic": topic, "content": res.text, "len": f"{m}분 {s}초"})
                st.success("✅ 생성 완료!")
                st.write(res.text)
            except Exception as e: st.error(f"서버 응답 지연: 다시 한번만 눌러주세요. ({e})")
        else: st.warning("설정에서 API 키를 먼저 확인해 주십시오.")

elif menu == "🤖 AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 (별 ☆ 클릭 시 즐겨찾기)")
    ai_list = ["Claude", "Gemini", "Grok", "ChatGPT", "Perplexity", "Midjourney", "Kling AI", "Sora"]
    cols = st.columns(4)
    for i, ai in enumerate(ai_list):
        with cols[i % 4]:
            is_fav = ai in st.session_state.fav_ai
            if st.button(f"{'⭐' if is_fav else '☆'} {ai}", key=ai):
                if is_fav: st.session_state.fav_ai.remove(ai)
                elif len(st.session_state.fav_ai) < 8: st.session_state.fav_ai.append(ai)
                st.rerun()

elif menu == "🔄 데이터 동기화":
    st.subheader("🔄 데이터 동기화")
    data = json.dumps({"fav": st.session_state.fav_ai, "hist": st.session_state.history}, indent=4)
    st.download_button("📤 데이터 내보내기", data=data, file_name="yt_backup.json")
    f = st.file_uploader("📥 데이터 가져오기", type="json")
    if f and st.button("✅ 복원 완료"):
        d = json.load(f)
        st.session_state.fav_ai, st.session_state.history = d['fav'], d['hist']
        st.success("복원 완료!")

else:
    st.subheader("⚙️ 설정 (API 키)")
    st.session_state.api_keys["Claude"] = st.text_input("Claude Key", value=st.session_state.api_keys["Claude"], type="password")
    st.session_state.api_keys["YouTube"] = st.text_input("YouTube Key", value=st.session_state.api_keys["YouTube"], type="password")
    if st.button("저장"): st.success("✅ 저장됨")
