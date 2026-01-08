import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------------
# Streamlit 요소 데모 페이지
# 모든 요소 예시와 학습용 각주(주석)를 포함합니다.
# 실행: `streamlit run streamlit_app.py`
# -----------------------------

st.set_page_config(
    page_title="Streamlit 요소 데모", page_icon="🎛️", layout="wide"
)

# 페이지 상단: 제목과 설명
st.title("🎛️ Streamlit 요소 데모 페이지")
st.write("이 페이지는 단일 페이지에 넣을 수 있는 Streamlit 요소들의 예시를 모아둔 학습용 데모입니다.")
st.caption("각 코드 블록 위에 설명(각주)이 있으니 따라가며 실습하세요.")

# 간단한 마크다운과 코드 표시
st.markdown("### 기본 텍스트 / 마크다운 / 코드 / 라텍스")
# 각주: `st.write`는 자동으로 타입을 판단해 렌더링합니다.
st.write("일반 텍스트 출력: Hello Streamlit!")
st.code("print('Hello Streamlit')", language="python")
st.latex(r"E = mc^2")  # 각주: KaTeX 수식 표시

# 상태 메시지들: success, info, warning, error
st.success("성공 메시지 예시")
st.info("정보 메시지 예시")
st.warning("경고 메시지 예시")
st.error("오류 메시지 예시")

# 레이아웃: 사이드바, 컬럼, 탭, 확장기
st.markdown("---")
st.markdown("## 레이아웃 구성 예시(divs)")

with st.sidebar:
    # 각주: 사이드바는 페이지 레이아웃과 독립적으로 상호작용 요소를 가집니다.
    st.header("사이드바")
    st.write("사이드바에 넣을 수 있는 위젯들")
    sidebar_choice = st.selectbox("사이드바 선택", ["옵션 A", "옵션 B", "옵션 C"]) 

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader("컬럼 1: 입력(폼/위젯)")
    # 입력 위젯 예시들
    if st.button("버튼 클릭" ):
        st.write("버튼이 클릭되었습니다")
    agree = st.checkbox("체크박스 선택")  # 각주: 체크박스는 불리언 값을 반환
    choice = st.radio("라디오 선택", ("사과", "바나나", "체리"))
    sel = st.selectbox("셀렉트박스", ["옵션 1", "옵션 2", "옵션 3"]) 
    multi = st.multiselect("멀티셀렉트", ["빨강", "초록", "파랑"], default=["빨강"]) 

with col2:
    st.subheader("컬럼 2: 슬라이더/입력")
    # 수치 입력 관련 위젯
    number = st.number_input("숫자 입력", min_value=0, max_value=100, value=10)
    text = st.text_input("한 줄 텍스트 입력", "여기에 입력")
    area = st.text_area("여러 줄 텍스트", "여러 줄 텍스트 예시")
    slider = st.slider("범위 슬라이더", 0, 100, (20, 80))
    select_slider = st.select_slider("선택 슬라이더", options=["초급", "중급", "고급"]) 

with col3:
    st.subheader("컬럼 3: 날짜/파일/색상")
    d = st.date_input("날짜 입력", datetime.now())
    t = st.time_input("시간 입력", datetime.now().time())
    uploaded = st.file_uploader("파일 업로드")
    color = st.color_picker("색 선택", "#00f900")

with st.expander("더 많은 레이아웃 요소 보기"):
    st.write("여기엔 `st.container()`, `st.empty()` 등을 넣을 수 있습니다.")
    placeholder = st.empty()  # 각주: 빈 자리(플레이스홀더)를 만들어 추후에 업데이트 가능
    placeholder.text("이 텍스트는 placeholder로 나중에 바꿀 수 있습니다.")

# 탭 예시
tab1, tab2 = st.tabs(["탭 A", "탭 B"])
with tab1:
    st.write("탭 A 내용")
with tab2:
    st.write("탭 B 내용")

st.markdown("---")

# 미디어: 이미지, 오디오, 비디오
st.markdown("## 미디어")
st.image("https://static.streamlit.io/examples/dice.jpg", caption="샘플 이미지")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
st.video("https://www.youtube.com/watch?v=JwSS70SZdyM")

st.markdown("---")

# 데이터 표시 및 차트
st.markdown("## 데이터와 차트")
df = pd.DataFrame(np.random.randn(50, 3), columns=["a", "b", "c"])  # 각주: 샘플 데이터
st.dataframe(df.head())  # 각주: 인터랙티브 데이터프레임
st.table(df.describe())

st.line_chart(df)
st.area_chart(df)
st.bar_chart(df.abs().head())

# 지도 예시 (위도/경도 데이터 필요)
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
)
st.map(map_data)

st.markdown("---")

# 차트 라이브러리 예시(선택적): Plotly/Altair 사용법은 추가 패키지가 필요합니다.

# 진행상태, 스피너, 메트릭
st.markdown("## 유틸리티: 진행상태, 스피너, 메트릭")
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)

with st.spinner("로딩 중..."):
    import time

    time.sleep(0.2)
st.success("로딩 완료")

st.metric(label="현재 온도", value="21°C", delta="+1.2°C")

st.markdown("---")

# 폼(form) 사용 예시
st.markdown("## 폼 (제출형 위젯)")
with st.form(key="my_form"):
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=0, max_value=120, value=30)
    submit = st.form_submit_button("제출")
    if submit:
        st.write(f"안녕하세요 {name}님, {age}세군요!")

# 캐시 사용 예시: @st.cache_data (데이터 캐싱)
@st.cache_data
def expensive_computation(n):
    # 각주: 시간이 오래 걸리는 연산을 시뮬레이션
    return np.random.randn(n, 2)

data = expensive_computation(1000)
st.write("캐시된 데이터 샘플:")
st.write(data[:5])

st.markdown("---")

# 세션 상태 예시
st.markdown("## 세션 상태 (상태 유지)")
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("세션 카운트 증가"):
    st.session_state.count += 1
st.write("세션 카운트:", st.session_state.count)

st.markdown("---")

st.write("데모 끝 — 각 위젯의 동작을 직접 바꿔보며 공부하세요.")

