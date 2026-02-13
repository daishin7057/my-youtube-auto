import streamlit as st
import google.generativeai as genai

# 클라우드 보안 설정(Secrets)에서 키를 가져오는 방식입니다.
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("대표님, 아직 API 키 설정이 되지 않았습니다. (Secrets 설정 필요)")

st.title("🤖 김 비서의 글로벌 유튜브 공장")
topic = st.text_input("쇼츠 주제를 입력하세요", placeholder="예: 배신하는 고양이 스토리")

if st.button("AI 보좌관 가동"):
    if topic:
        with st.spinner("최상의 대본을 작성 중입니다..."):
            response = model.generate_content(f"{topic} 주제로 유튜브 쇼츠 대본 써줘")
            st.success("대본 작성이 완료되었습니다!")
            st.markdown("---")
            st.write(response.text)
    else:
        st.warning("주제를 입력해 주셔야 일을 시작할 수 있습니다.")
import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# --- 초기 설정 및 보안 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("대표님, 비밀 금고에 API 키가 없습니다!")

st.set_page_config(page_title="김 비서의 글로벌 유튜브 공장 v3.0", layout="wide")

# --- 데이터 저장소 (Session State) ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 기능 함수: 트렌드 분석 ---
def get_trending_topics():
    # 실제 실시간 API 연결 전, AI 기반 트렌드 예측 로직
    prompt = "최근 3개월 내 유튜브에서 조회수 100만 이상을 기록한 핫한 쇼츠 및 롱폼 주제 5가지를 분석해서 추천해줘."
    res = model.generate_content(prompt)
    return res.text

# --- 사이드바: AI 도구 시트 및 설정 ---
with st.sidebar:
    st.header("📂 공장 관리 데스크")
    menu = st.radio("이동할 구역", ["콘텐츠 제작실", "실시간 트렌드 센터", "AI 도구 백서"])
    
    st.divider()
    st.subheader("🛠️ 제작 설정")
    content_type = st.selectbox("제작 유형", ["숏폼 (Shorts)", "롱폼 (Long-form)"])
    
    if st.button("🔄 트렌드 데이터 갱신"):
        st.session_state.trends = get_trending_topics()

# --- 1구역: AI 도구 백서 (Resource Sheet) ---
if menu == "AI 도구 백서":
    st.title("📚 AI 프로그램 사이트 검색 시트")
    ai_tools = {
        "카테고리": ["언어 모델", "언어 모델", "이미지 생성", "영상 생성", "워크플로우"],
        "프로그램명": ["Gemini", "Claude", "Grok", "Flux / Midjourney", "Flow / LangChain"],
        "주요 용도": ["구글 생태계 연동, 대본", "코딩 및 정교한 글쓰기", "X(트위터) 기반 실시간 정보", "고퀄리티 이미지 제작", "AI 자동화 프로세스 설계"],
        "링크": ["https://gemini.google.com", "https://claude.ai", "https://x.ai", "https://midjourney.com", "https://flowiseai.com"]
    }
    df = pd.DataFrame(ai_tools)
    st.table(df)

# --- 2구역: 실시간 트렌드 센터 ---
elif menu == "실시간 트렌드 센터":
    st.title("🔥 실시간 유튜브 트렌드 분석")
    st.info("최근 3개월 내 조회수 100만 이상의 인기 키워드를 분석합니다.")
    if 'trends' in st.session_state:
        st.markdown(st.session_state.trends)
    else:
        st.write("측면 메뉴의 '트렌드 데이터 갱신' 버튼을 눌러주십시오.")

# --- 3구역: 콘텐츠 제작실 (CRUD 기능 포함) ---
else:
    st.title("🎬 콘텐츠 제작 및 관리")
    
    # 제작 프로세스 확인용 Expander
    with st.expander("🔍 대본이 어떻게 만들어지나요? (프롬프트 구조 보기)"):
        st.code("""
        1. 주제 분석 -> 2. 타겟 맞춤형 톤 설정 -> 3. 후킹 문구 생성 
        -> 4. 장면별 시각 묘사(Image Prompt) 추출 -> 5. 최종 검수
        """)

    # 입력창
    topic = st.text_input("새로운 주제를 입력하세요", placeholder="예: 고양이의 복수")
    
    if st.button("🚀 AI 보좌관 가동"):
        if topic:
            with st.spinner("최상의 대본을 집필 중입니다..."):
                response = model.generate_content(f"{topic} 주제로 {content_type} 대본 써줘")
                new_data = {
                    "id": len(st.session_state.history),
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": content_type,
                    "topic": topic,
                    "content": response.text
                }
                st.session_state.history.insert(0, new_data) # 최신글이 위로

    st.divider()
    
    # 작업 관리자 (Edit / Delete)
    st.subheader("📂 최근 작업 히스토리")
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"[{item['time']}] {item['topic']} ({item['type']})"):
            # 내용 수정
            edited_content = st.text_area("내용 수정", item['content'], key=f"edit_{idx}", height=200)
            if st.button("💾 수정 내용 저장", key=f"save_{idx}"):
                st.session_state.history[idx]['content'] = edited_content
                st.success("수정되었습니다!")
            
            # 삭제 버튼
            if st.button("🗑️ 이 작업 삭제", key=f"del_{idx}"):
                st.session_state.history.pop(idx)
                st.rerun()
                import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
from datetime import datetime

# --- 1. 보안 및 초기 설정 ---
st.set_page_config(page_title="YT Creator Studio Pro", layout="wide", initial_sidebar_state="expanded")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("보안 설정(Secrets)에 API 키가 없습니다.")

# 데이터 저장소 초기화
for key in ['fav_ai', 'history', 'saved_vault', 'api_keys']:
    if key not in st.session_state:
        st.session_state[key] = [] if key != 'api_keys' else {"Gemini": "", "YouTube": ""}

# --- 2. 커스텀 CSS (다크 테마 디자인) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    .trend-card { background-color: #161b22; padding: 10px; border-radius: 8px; margin-bottom: 5px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 내비게이션 ---
with st.sidebar:
    st.title("🎬 YT Studio Pro")
    st.caption("AI 영상 자동화 플랫폼")
    menu = st.radio("메인 메뉴", ["🏠 대시보드", "🔥 트렌드 분석", "✨ 콘텐츠 생성", "⚙️ 9단계 파이프라인", "📁 내 프로젝트", "🤖 AI 검색엔진", "🔄 데이터 동기화"])
    st.divider()
    st.info(f"서버 상태: ✅ 운영 중\n현재 날짜: {datetime.now().strftime('%Y-%m-%d')}")

# --- 4. 페이지 구성 ---

# [4-1] 대시보드 (image_a374a0.png 레이아웃 재현)
if menu == "🏠 대시보드":
    # 상단 요약 지표
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 트렌드 키워드", "847", "↑ 실시간 업데이트")
    col2.metric("🎬 생성 완료 영상", "24", "↑ 이번 달 +8")
    col3.metric("⚡ 진행 중 파이프라인", "3", "Step 3/9 진행 중")
    col4.metric("🔥 핫 트렌드 발견", "18", "↑ 100만+ 조회 영상")

    st.divider()
    
    mid_col1, mid_col2 = st.columns([1.5, 1])
    
    with mid_col1:
        st.subheader("🔥 실시간 핫 트렌드 (3개월 이내 · 100만+ 조회)")
        trends = [
            {"rank": 1, "title": "고양이가 스시 만드는 법 (진짜임)", "views": "4,230만", "tag": "쇼츠"},
            {"rank": 2, "title": "폐허 속에서 발견한 비밀 지하 도시", "views": "3,870만", "tag": "롱폼"},
            {"rank": 3, "title": "AI로 만든 완벽한 로맨스 영화 60초", "views": "2,940만", "tag": "쇼츠"}
        ]
        for t in trends:
            st.markdown(f"""
            <div class="trend-card">
                <b>{t['rank']}. {t['title']}</b><br>
                <small>조회수: {t['views']} | 유형: {t['tag']}</small>
            </div>
            """, unsafe_allow_html=True)
            
    with mid_col2:
        st.subheader("⚙️ 파이프라인 현황")
        steps = ["트렌드 분석", "주제 확정", "대본 생성", "이미지 프롬프트", "이미지 생성", "음성 합성(TTS)", "영상 편집", "최종 검수", "자동 업로드"]
        for i, step in enumerate(steps):
            status = "✅" if i < 2 else ("⏳" if i == 2 else "⚪")
            st.write(f"{status} {i+1}. {step}")

# [4-2] 콘텐츠 생성
elif menu == "✨ 콘텐츠 생성":
    st.subheader("🎯 맞춤형 콘텐츠 기획")
    duration = st.select_slider("영상 길이 설정", options=["15초", "60초", "3분", "10분", "30분"], value="60초")
    topic = st.text_input("주제", placeholder="예: 2차대전 탱크 복원 스토리")
    
    if st.button("🚀 AI 보좌관 가동"):
        if topic:
            with st.spinner("최상의 대본과 프롬프트를 집필 중..."):
                res = model.generate_content(f"{topic} 주제로 {duration} 분량의 유튜브 대본, 이미지 프롬프트 3개, 태그 5개를 써줘.")
                st.session_state.last_res = {"topic": topic, "content": res.text, "duration": duration}
                st.markdown(res.text)
        else: st.warning("주제를 입력하세요.")

    if 'last_res' in st.session_state:
        st.divider()
        video_url = st.text_input("🔗 완성 영상 링크 저장 (선택 사항)")
        if st.button("📥 내 프로젝트(저장고)에 보관"):
            st.session_state.saved_vault.insert(0, {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "topic": st.session_state.last_res['topic'],
                "content": st.session_state.last_res['content'],
                "url": video_url if video_url else "기록 없음"
            })
            st.success("대표님 전용 저장고에 안전하게 보관되었습니다!")

# [4-3] 내 프로젝트 (저장 공간)
elif menu == "📁 내 프로젝트":
    st.subheader("🔒 대표님 전용 콘텐츠 저장고")
    if not st.session_state.saved_vault:
        st.info("아직 저장된 콘텐츠가 없습니다.")
    else:
        for idx, item in enumerate(st.session_state.saved_vault):
            with st.expander(f"📌 [{item['date']}] {item['topic']}"):
                st.write("**📝 프롬프트 및 대본:**")
                st.code(item['content'])
                st.write(f"**🔗 영상 주소:** {item['url']}")
                if st.button("🗑️ 삭제", key=f"del_{idx}"):
                    st.session_state.saved_vault.pop(idx)
                    st.rerun()

# [4-4] AI 검색엔진
elif menu == "🤖 AI 검색엔진":
    st.subheader("🤖 글로벌 AI 엔진 빠른 접속")
    cols = st.columns(4)
    ai_list = [("Claude", "Anthropic"), ("Gemini", "Google"), ("Grok", "xAI"), ("ChatGPT", "OpenAI")]
    for i, (name, prov) in enumerate(ai_list):
        cols[i % 4].button(f"🔗 {name}\n({prov})")

# [4-5] 데이터 동기화
elif menu == "🔄 데이터 동기화":
    st.subheader("🔄 집/회사 데이터 동기화")
    data_str = json.dumps({
        "saved_vault": st.session_state.saved_vault,
        "fav_ai": st.session_state.fav_ai
    }, indent=4)
    st.download_button("📤 전체 데이터 내보내기 (JSON)", data=data_str, file_name="yt_studio_backup.json")
    
    file = st.file_uploader("📥 데이터 가져오기", type="json")
    if file and st.button("✅ 데이터 복원"):
        imported = json.load(file)
        st.session_state.saved_vault = imported.get("saved_vault", [])
        st.success("모든 프로젝트 데이터가 복원되었습니다!")

            st.markdown("---")
            st.write(item['content'])
import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
from datetime import datetime

# --- 1. 페이지 및 보안 설정 ---
st.set_page_config(page_title="YT Creator Studio Pro", layout="wide", initial_sidebar_state="expanded")

# CSS: 대표님이 보내주신 이미지의 다크 테마와 카드 디자인 재현
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 12px; border: 1px solid #3b82f6; }
    .card { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .trend-item { background: #1c2128; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #f78166; }
    .sidebar .sidebar-content { background-image: linear-gradient(#161b22, #0e1117); }
    </style>
    """, unsafe_allow_html=True)

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("보안 설정(Secrets)에 API 키가 없습니다.")

# 데이터 저장소 초기화
for key in ['saved_vault', 'fav_ai']:
    if key not in st.session_state: st.session_state[key] = []

# --- 2. 사이드바 내비게이션 (이미지 구성 재현) ---
with st.sidebar:
    st.title("🎬 YT Studio Pro")
    st.caption("AI 영상 자동화 플랫폼")
    menu = st.radio("메인 메뉴", ["🏠 대시보드", "🔥 트렌드 분석", "✨ 콘텐츠 생성", "⚙️ 9단계 파이프라인", "📂 내 프로젝트", "🤖 AI 검색엔진", "🔄 데이터 동기화"])
    st.divider()
    st.info(f"서버 상태: ✅ 온라인\n접속 시각: {datetime.now().strftime('%H:%M:%S')}")

# --- 3. 각 페이지별 기능 구현 ---

# [3-1] 대시보드 (지표 카드 및 트렌드 리스트)
if menu == "🏠 대시보드":
    st.header("대시보드")
    
    # 상단 요약 지표 카드 (image_a374a0.png 재현)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 트렌드 키워드", "847", "↑ 실시간")
    col2.metric("🎬 생성 완료 영상", "24", "↑ 이번 달 +8")
    col3.metric("⚡ 파이프라인", "Step 3/9", "진행 중")
    col4.metric("🔥 핫 트렌드", "18건", "↑ 100만+ 조회")

    st.divider()

    mid_col1, mid_col2 = st.columns([1.5, 1])
    
    with mid_col1:
        st.subheader("🔥 실시간 핫 트렌드 (100만+ 조회)")
        trends = [
            {"rank": 1, "title": "고양이가 스시 만드는 법 (진짜임)", "views": "4,230만", "tag": "쇼츠"},
            {"rank": 2, "title": "폐허 속에서 발견한 비밀 지하 도시", "views": "3,870만", "tag": "롱폼"},
            {"rank": 3, "title": "AI로 만든 완벽한 로맨스 영화 60초", "views": "2,940만", "tag": "쇼츠"}
        ]
        for t in trends:
            st.markdown(f"""
            <div class="trend-item">
                <b>{t['rank']}. {t['title']}</b><br>
                <small>조회수: {t['views']} | 유형: {t['tag']}</small>
            </div>
            """, unsafe_allow_html=True)
            
    with mid_col2:
        st.subheader("⚙️ 파이프라인 현황")
        steps = ["트렌드 분석", "주제 확정", "대본 생성", "이미지 프롬프트", "이미지 생성", "음성 합성(TTS)", "영상 편집", "최종 검수", "자동 업로드"]
        for i, step in enumerate(steps):
            status = "✅" if i < 2 else ("⏳" if i == 2 else "⚪")
            st.write(f"{status} {i+1}. {step}")

# [3-2] 콘텐츠 생성 및 저장고 기능
elif menu == "✨ 콘텐츠 생성":
    st.subheader("🎯 맞춤형 콘텐츠 기획")
    with st.container():
        duration = st.select_slider("영상 길이", options=["15초", "60초", "3분", "10분", "30분"], value="60초")
        topic = st.text_input("주제", placeholder="예: 2차대전 탱크 복원 스토리")
        
        if st.button("🚀 AI 보좌관 가동"):
            if topic:
                with st.spinner("AI가 정교한 대본을 생성 중입니다..."):
                    res = model.generate_content(f"{topic} 주제로 {duration} 분량의 대본과 이미지 프롬프트 써줘.")
                    st.session_state.last_res = {"topic": topic, "content": res.text}
                    st.markdown(res.text)
            else: st.warning("주제를 입력하세요.")

    if 'last_res' in st.session_state:
        st.divider()
        video_url = st.text_input("🔗 완성 영상 링크 저장", placeholder="https://youtube.com/...")
        if st.button("📥 내 프로젝트에 영구 보관"):
            st.session_state.saved_vault.insert(0, {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "topic": st.session_state.last_res['topic'],
                "content": st.session_state.last_res['content'],
                "url": video_url if video_url else "링크 없음"
            })
            st.success("대표님 전용 금고에 저장되었습니다!")

# [3-3] AI 검색엔진 (퀵 액세스 카드)
elif menu == "🤖 AI 검색엔진":
    st.subheader("🤖 AI 검색엔진 빠른 접속")
    cols = st.columns(4)
    ai_list = [("Claude", "Anthropic"), ("Gemini", "Google"), ("Grok", "xAI"), ("ChatGPT", "OpenAI")]
    for i, (name, prov) in enumerate(ai_list):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:#1e2130; padding:20px; border-radius:10px; text-align:center;">
                <h3>{name}</h3><p>{prov}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"접속 {name}", key=f"btn_{name}")

# [3-4] 데이터 동기화
elif menu == "🔄 데이터 동기화":
    st.subheader("🔄 집/회사 데이터 동기화")
    data_str = json.dumps({"vault": st.session_state.saved_vault}, indent=4)
    st.download_button("📤 데이터 내보내기 (JSON)", data=data_str, file_name="yt_studio_pro_backup.json")
    file = st.file_uploader("📥 데이터 가져오기", type="json")
    if file and st.button("✅ 데이터 복원"):
        st.session_state.saved_vault = json.load(file).get("vault", [])
        st.success("모든 설정과 저장물이 복원되었습니다!")
