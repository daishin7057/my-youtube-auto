import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
from datetime import datetime

# --- 1. 페이지 및 보안 설정 ---
st.set_page_config(page_title="YT Creator Studio Pro", layout="wide", initial_sidebar_state="expanded")

# CSS: 다크 테마 디자인 구현
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 12px; border: 1px solid #3b82f6; }
    .card { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .trend-item { background: #1c2128; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #f78166; }
    </style>
    """, unsafe_allow_html=True)

# API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("대표님, 보안 설정(Secrets)에 API 키가 없습니다!")

# 데이터 저장소 초기화
if 'saved_vault' not in st.session_state: st.session_state.saved_vault = []
if 'fav_ai' not in st.session_state: st.session_state.fav_ai = []

# --- 2. 사이드바 내비게이션 ---
with st.sidebar:
    st.title("🎬 YT Studio Pro")
    menu = st.radio("메인 메뉴", ["🏠 대시보드", "🔥 트렌드 분석", "✨ 콘텐츠 생성", "⚙️ 9단계 파이프라인", "📁 내 프로젝트", "🤖 AI 검색엔진", "🔄 데이터 동기화"])
    st.divider()
    st.info(f"서버 상태: ✅ 온라인\n날짜: {datetime.now().strftime('%Y-%m-%d')}")

# --- 3. 각 페이지별 기능 ---

# [3-1] 대시보드
if menu == "🏠 대시보드":
    st.header("종합 관제 대시보드")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 트렌드 키워드", "847", "↑")
    col2.metric("🎬 생성 완료", f"{len(st.session_state.saved_vault)}건", "+1")
    col3.metric("⚡ 파이프라인", "Step 3/9", "진행중")
    col4.metric("🔥 핫 트렌드", "18건", "NEW")

    st.divider()
    m_col1, m_col2 = st.columns([1.5, 1])
    with m_col1:
        st.subheader("🔥 실시간 트렌드 리스트")
        for i, t in enumerate(["고양이 스시 제작기", "비밀 지하 도시 탐험", "AI 로맨스 60초"]):
            st.markdown(f"<div class='trend-item'><b>{i+1}. {t}</b></div>", unsafe_allow_html=True)
    with m_col2:
        st.subheader("⚙️ 제작 공정 현황")
        for step in ["분석", "주제", "대본", "이미지", "영상", "TTS", "편집", "검수", "업로드"]:
            st.write(f"⚪ {step}")

# [3-2] 콘텐츠 생성
elif menu == "✨ 콘텐츠 생성":
    st.subheader("🎯 콘텐츠 기획 및 제작")
    duration = st.select_slider("길이 설정", options=["15초", "60초", "3분", "10분"], value="60초")
    topic = st.text_input("주제 입력", placeholder="예: 탱크 복원 스토리")
    
    if st.button("🚀 AI 가동"):
        if topic:
            with st.spinner("집필 중..."):
                res = model.generate_content(f"{topic} 주제로 {duration} 유튜브 대본 써줘.")
                st.session_state.last_res = {"topic": topic, "content": res.text}
                st.markdown(res.text)
        else: st.warning("주제를 입력하세요.")

    if 'last_res' in st.session_state:
        st.divider()
        url = st.text_input("🔗 영상 링크 (선택)")
        if st.button("📥 프로젝트 저장고로 보관"):
            st.session_state.saved_vault.insert(0, {"date": datetime.now().strftime("%m-%d"), "topic": st.session_state.last_res['topic'], "content": st.session_state.last_res['content'], "url": url})
            st.success("보관 완료!")

# [3-3] 내 프로젝트
elif menu == "📁 내 프로젝트":
    st.subheader("📁 내 콘텐츠 저장고")
    for idx, item in enumerate(st.session_state.saved_vault):
        with st.expander(f"📌 {item['date']} - {item['topic']}"):
            st.code(item['content'])
            st.write(f"링크: {item['url']}")
            if st.button("🗑️ 삭제", key=f"del_{idx}"):
                st.session_state.saved_vault.pop(idx)
                st.rerun()

# [3-4] 나머지 메뉴 (간략 구현)
else:
    st.write(f"{menu} 페이지는 현재 준비 중입니다.")
