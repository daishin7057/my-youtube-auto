import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

# --- 1. 환경 설정 및 보안 ---
st.set_page_config(page_title="YT Creator Studio Pro", layout="wide", initial_sidebar_state="expanded")

# 프리미엄 다크 테마 CSS 적용
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e2130; padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    div[data-testid="stExpander"] { background-color: #161b22; border-radius: 10px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #3b82f6; color: white; border: none; height: 3em; font-weight: bold; }
    .stButton>button:hover { background-color: #2563eb; border: none; }
    .sidebar .sidebar-content { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# API 키 인증
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Secrets 설정에서 API 키를 확인해주세요!")

# 저장소 초기화
if 'saved_vault' not in st.session_state: st.session_state.saved_vault = []

# --- 2. 사이드바 제어 센터 ---
with st.sidebar:
    st.title("🎬 YT Studio Pro")
    st.caption("CEO 전용 콘텐츠 관제 시스템")
    st.divider()
    menu = st.radio("메뉴 이동", ["🏠 대시보드", "✨ 콘텐츠 제작", "📦 프로젝트 금고", "🔄 데이터 관리"])
    st.divider()
    st.success(f"상태: ✅ 가동 중\n{datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- 3. 페이지별 기능 구현 ---

# [3-1] 대시보드 (통계 및 트렌드)
if menu == "🏠 대시보드":
    st.header("종합 관제 대시보드")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 트렌드 지수", "847", "↑ 12%")
    col2.metric("🎬 제작 영상", f"{len(st.session_state.saved_vault)}건", "+1")
    col3.metric("⚡ 파이프라인", "Step 3/9", "진행중")
    col4.metric("🔥 인기 키워드", "18건", "NEW")
    
    st.divider()
    
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("🔥 실시간 핫 트렌드 (100만+)")
        trends = ["고양이가 스시 만드는 법", "2차대전 탱크 복원 비하인드", "AI가 그린 완벽한 로맨스"]
        for i, t in enumerate(trends):
            st.info(f"{i+1}. {t}")
    with c2:
        st.subheader("⚙️ 제작 공정 현황")
        steps = ["분석", "주제", "대본", "이미지", "영상", "TTS", "편집", "검수", "업로드"]
        for idx, s in enumerate(steps):
            icon = "✅" if idx < 2 else ("⏳" if idx == 2 else "⚪")
            st.write(f"{icon} {idx+1}. {s}")

# [3-2] 콘텐츠 제작 (타임라인 정밀 설정)
elif menu == "✨ 콘텐츠 제작":
    st.subheader("🎯 정밀 콘텐츠 기획")
    
    # 대표님 요청: 쇼츠와 롱폼 타임라인 분리 설정
    c_type = st.segmented_control("제작 유형", ["숏폼(Shorts)", "롱폼(Long-form)"], default="숏폼(Shorts)")
    
    if c_type == "숏폼(Shorts)":
        duration = st.select_slider("⏱️ 쇼츠 타임라인 (초)", options=["15초", "30초", "60초"], value="60초")
    else:
        duration = st.select_slider("⏱️ 롱폼 타임라인 (분)", options=["3분", "5분", "10분", "30분"], value="10분")
    
    topic = st.text_input("콘텐츠 주제", placeholder="예: 곰을 배신한 고양이의 반전")
    
    if st.button("🚀 AI 보좌관 가동"):
        if topic:
            with st.spinner(f"{duration} 분량의 최상급 대본을 집필 중입니다..."):
                prompt = f"{topic} 주제로 유튜브 {c_type} 대본과 이미지 프롬프트 써줘. 길이는 {duration}에 맞춰줘."
                res = model.generate_content(prompt)
                st.session_state.last_work = {"topic": topic, "content": res.text, "type": c_type, "len": duration}
                st.markdown("### 📝 생성된 대본")
                st.write(res.text)
        else: st.warning("주제를 입력하셔야 일을 시작합니다.")

    if 'last_work' in st.session_state:
        st.divider()
        v_url = st.text_input("🔗 완성 영상 링크 (저장용)")
        if st.button("📥 이 프로젝트를 금고에 보관"):
            data = st.session_state.last_work
            st.session_state.saved_vault.insert(0, {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "topic": data['topic'], "content": data['content'],
                "type": data['type'], "len": data['len'], "url": v_url
            })
            st.success("대표님 전용 금고에 안전하게 저장되었습니다!")

# [3-3] 프로젝트 금고
elif menu == "📦 프로젝트 금고":
    st.subheader("📦 보관된 콘텐츠 리스트")
    if not st.session_state.saved_vault:
        st.info("아직 저장된 프로젝트가 없습니다.")
    else:
        for idx, item in enumerate(st.session_state.saved_vault):
            with st.expander(f"📌 [{item['date']}] {item['topic']} ({item['type']} / {item['len']})"):
                st.code(item['content'])
                st.write(f"영상 링크: {item['url']}")
                if st.button("🗑️ 삭제", key=f"del_{idx}"):
                    st.session_state.saved_vault.pop(idx)
                    st.rerun()

# [3-4] 데이터 관리
else:
    st.subheader("🔄 데이터 동기화")
    data_str = json.dumps(st.session_state.saved_vault, indent=4)
    st.download_button("📤 전체 데이터 내보내기 (JSON)", data=data_str, file_name="yt_studio_backup.json")
    f = st.file_uploader("📥 데이터 가져오기", type="json")
    if f and st.button("✅ 데이터 복구"):
        st.session_state.saved_vault = json.load(f)
        st.success("모든 데이터가 완벽하게 복원되었습니다!")
