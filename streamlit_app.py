import streamlit as st
import random
import time

# 간단한 암산 루틴 앱 (초등 5학년용)
# 흐름: 문제 제시 -> 3초 암산 -> 정답 표시 -> 3초 후 다음 문제 자동 진행

st.set_page_config(page_title="암산 루틴 (초등 5학년)", page_icon="🧠", layout="centered")

st.title("🧮 암산 루틴 - 초등 5학년")
st.write("자동 반복형 암산 연습: 문제 제시 → 3초 암산 → 정답 표시 → 3초 후 다음 문제")

# 사이드바 옵션
st.sidebar.header("설정")
num_questions = st.sidebar.number_input("문제 수", min_value=1, max_value=100, value=20)
ops = st.sidebar.multiselect("연산", ["덧셈", "뺄셈", "곱셈"], default=["덧셈", "뺄셈", "곱셈"]) 

# 세션 상태 초기화
if "running" not in st.session_state:
    st.session_state.running = False
if "index" not in st.session_state:
    st.session_state.index = 0

# 문제 생성기 (간단한 구현)
def generate_problem():
    op = random.choice(ops)
    if op == "덧셈":
        a = random.randint(10, 999)
        b = random.randint(10, 999)
        return f"{a} + {b}", a + b
    if op == "뺄셈":
        a = random.randint(20, 999)
        b = random.randint(10, a)
        return f"{a} - {b}", a - b
    # 곱셈
    a = random.randint(2, 99)
    b = random.randint(2, 9)
    return f"{a} × {b}", a * b

# 시작 버튼
if st.button("시작"):
    if not ops:
        st.warning("최소 하나의 연산을 선택하세요.")
    else:
        st.session_state.running = True
        st.session_state.index = 0

placeholder = st.empty()
progress = st.empty()

# 루프 실행 (간단한 blocking 방식)
if st.session_state.running:
    try:
        for i in range(st.session_state.index, num_questions):
            q, ans = generate_problem()
            placeholder.markdown(f"### 문제 {i+1} / {num_questions}")
            placeholder.markdown(f"<h1 style='text-align:center'>{q}</h1>", unsafe_allow_html=True)

            # 3초 카운트다운(암산)
            for s in range(3, 0, -1):
                placeholder.markdown(f"<h2 style='text-align:center'>암산: {s}</h2>", unsafe_allow_html=True)
                time.sleep(1)

            # 정답 표시
            placeholder.markdown(f"<h1 style='text-align:center;color:green'>정답: {ans}</h1>", unsafe_allow_html=True)

            # 3초 대기 후 다음 문제
            for s in range(3, 0, -1):
                placeholder.markdown(f"<h3 style='text-align:center'>다음 문제까지: {s}</h3>", unsafe_allow_html=True)
                time.sleep(1)

            st.session_state.index = i + 1
            progress.write(f"진행: {st.session_state.index} / {num_questions}")

        st.success("세션 완료! 잘하셨어요 🎉")
        st.session_state.running = False
    except Exception as e:
        st.error(f"오류 발생: {e}")
        st.session_state.running = False
else:
    st.info("사이드바에서 옵션을 선택하고 '시작'을 누르세요.")

