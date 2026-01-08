import streamlit as st
import random
import time
from datetime import timedelta

st.set_page_config(page_title="5학년 암산 연습", page_icon="🧠", layout="centered")

# -----------------------------
# 5학년 대상 암산(mental math) 학습 앱
# 기능:
# - 난이도(쉬움/보통/어려움)
# - 연산 선택(덧셈/뺄셈/곱셈/나눗셈)
# - 문제 수와 시간 제한(선택 가능)
# - 채점, 힌트, 정답/오답 기록, 통계
# -----------------------------

TITLE = "🧠 5학년 암산 연습"
st.title(TITLE)
st.write("짧고 집중된 문제로 암산 실력을 키워보세요. 각 문제를 가능한 빠르고 정확하게 푸는 것이 목표입니다.")

# 설정
st.sidebar.header("설정 🔧")
difficulty = st.sidebar.selectbox("난이도", ["쉬움", "보통", "어려움"])
ops = st.sidebar.multiselect("연산 선택", ["덧셈", "뺄셈", "곱셈", "나눗셈"], default=["덧셈", "뺄셈", "곱셈"])
num_questions = st.sidebar.number_input("문제 수", min_value=5, max_value=50, value=10)
use_timer = st.sidebar.checkbox("시간 제한 사용 (문제별)", value=False)
per_question_time = st.sidebar.slider("문제별 시간(초)", min_value=5, max_value=60, value=20)
show_hints = st.sidebar.checkbox("힌트 보기", value=True)

# 난이도별 숫자 범위
RANGES = {
    "쉬움": (0, 50),
    "보통": (0, 200),
    "어려움": (0, 1000),
}
min_val, max_val = RANGES[difficulty]

# 세션 상태 초기화
if "problems" not in st.session_state:
    st.session_state.problems = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "current" not in st.session_state:
    st.session_state.current = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "times" not in st.session_state:
    st.session_state.times = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "running" not in st.session_state:
    st.session_state.running = False

# 문제 생성기
def generate_problem():
    op = random.choice(ops)
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)

    # 나눗셈은 정수 몫 또는 간단한 분수로 만듦 (나눗셈 방지: b != 0)
    if op == "나눗셈":
        b = random.randint(1, max(1, max_val))
        # 답이 정수가 되도록 a를 b의 배수로 바꿈 (쉬움/보통) 또는 정수/한자리 소수 허용
        if difficulty == "쉬움":
            b_small = random.randint(1, 12)
            a = b_small * random.randint(1, 12)
            b = b_small
        else:
            # 보통/어려움은 나눗셈 결과를 소수 셋째자리에서 반올림
            a = random.randint(min_val, max_val)
            b = random.randint(1, max(1, max_val))
    elif op == "곱셈":
        if difficulty == "쉬움":
            a = random.randint(2, 12)
            b = random.randint(2, 12)
        elif difficulty == "보통":
            a = random.randint(2, 20)
            b = random.randint(2, 20)
        else:
            a = random.randint(10, 50)
            b = random.randint(2, 20)
    else:
        # 덧셈/뺄셈 기본
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)

    # 정답 계산
    if op == "덧셈":
        ans = a + b
        text = f"{a} + {b} = ?"
    elif op == "뺄셈":
        ans = a - b
        text = f"{a} − {b} = ?"
    elif op == "곱셈":
        ans = a * b
        text = f"{a} × {b} = ?"
    else:  # 나눗셈
        # 보통/어려움은 소수로 표현
        if difficulty == "쉬움":
            ans = a // b
            text = f"{a} ÷ {b} = ?  (정수 몫)"
        else:
            ans = round(a / b, 2)
            text = f"{a} ÷ {b} = ?  (소수 둘째자리까지 반올림)"

    hint = None
    if show_hints:
        if op == "덧셈":
            hint = "큰 자리부터 더해보세요. 일의 자리부터 계산 후 올림을 확인하세요."
        elif op == "뺄셈":
            hint = "뒤에서부터 빌려서 계산하세요. 음수인지 아닌지 먼저 생각해보세요."
        elif op == "곱셈":
            hint = "분해해서 계산해보세요. 예: 12×9 = 12×10 − 12"
        else:
            hint = "나눗셈은 나눗수를 곱해서 확인하거나 소수 자릿수를 정하세요."

    return {"text": text, "answer": ans, "op": op, "hint": hint}

# 시작 버튼
if st.button("새로운 세션 시작 🚀"):
    if not ops:
        st.warning("최소한 하나의 연산을 선택하세요.")
    else:
        st.session_state.problems = [generate_problem() for _ in range(num_questions)]
        st.session_state.answers = [None] * num_questions
        st.session_state.current = 0
        st.session_state.score = 0
        st.session_state.times = [None] * num_questions
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.experimental_rerun()

# 채점/입력 영역
if st.session_state.running and st.session_state.problems:
    idx = st.session_state.current
    problem = st.session_state.problems[idx]

    st.markdown(f"### 문제 {idx + 1} / {len(st.session_state.problems)}")
    st.write(problem["text"])

    if show_hints and problem.get("hint"):
        with st.expander("힌트 🔎"):
            st.write(problem["hint"])

    # 타이머
    time_start_q = st.session_state.times[idx] if st.session_state.times[idx] else None
    if use_timer:
        if f"timer_{idx}" not in st.session_state:
            st.session_state[f"timer_{idx}"] = per_question_time
        timer_placeholder = st.empty()
        # 타이머 감소(비동기는 아님 — 페이지 새로고침 시 갱신 필요)
        st.session_state[f"timer_{idx}"] = max(0, st.session_state[f"timer_{idx}"])
        timer_placeholder.markdown(f"⏱️ 남은 시간: **{st.session_state[f'timer_{idx}']}초**")

    user_input = st.text_input("정답을 입력하세요", key=f"input_{idx}")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("제출 ✅", key=f"submit_{idx}"):
            # 시간 기록
            elapsed = 0
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
            st.session_state.times[idx] = elapsed

            # 정답 비교
            try:
                # 나눗셈 소수/정수 비교
                if problem["op"] == "나눗셈" and difficulty != "쉬움":
                    user_ans = round(float(user_input), 2)
                else:
                    user_ans = int(float(user_input))
            except Exception:
                st.error("숫자를 입력해 주세요 (예: 42 또는 3.14).")
                user_ans = None

            correct = False
            if user_ans is not None:
                if isinstance(problem["answer"], float):
                    correct = abs(problem["answer"] - user_ans) < 0.01
                else:
                    correct = (problem["answer"] == user_ans)

            if correct:
                st.success("정답입니다! 🎉")
                st.session_state.score += 1
            else:
                st.error(f"틀렸습니다. 정답: {problem['answer']}")

            st.session_state.answers[idx] = {"given": user_ans, "correct": correct}
            # 다음 문제 이동
            if idx + 1 < len(st.session_state.problems):
                st.session_state.current += 1
                # reset per-question timer
                if use_timer:
                    st.session_state[f"timer_{idx + 1}"] = per_question_time
                st.experimental_rerun()
            else:
                st.session_state.running = False
                st.experimental_rerun()

    with col_b:
        if st.button("포기하고 답 보기 ❌", key=f"skip_{idx}"):
            st.warning(f"정답: {problem['answer']}")
            st.session_state.answers[idx] = {"given": None, "correct": False}
            if idx + 1 < len(st.session_state.problems):
                st.session_state.current += 1
                if use_timer:
                    st.session_state[f"timer_{idx + 1}"] = per_question_time
                st.experimental_rerun()
            else:
                st.session_state.running = False
                st.experimental_rerun()

    # 자동 타임아웃 처리(간단한 형태)
    if use_timer and st.session_state[f"timer_{idx}"] == 0 and st.session_state.answers[idx] is None:
        st.warning("시간 초과! 다음 문제로 이동합니다.")
        st.session_state.answers[idx] = {"given": None, "correct": False}
        if idx + 1 < len(st.session_state.problems):
            st.session_state.current += 1
            st.session_state[f"timer_{idx + 1}"] = per_question_time
            st.experimental_rerun()
        else:
            st.session_state.running = False
            st.experimental_rerun()

# 타이머 감소(페이지 상호작용 시마다 1초씩 감소 시뮬레이션)
for i in range(len(st.session_state.problems)):
    if use_timer and f"timer_{i}" in st.session_state and st.session_state[f"timer_{i}"] > 0 and st.session_state.current == i:
        st.session_state[f"timer_{i}"] = st.session_state[f"timer_{i}"] - 1

# 결과 요약
if not st.session_state.running and st.session_state.problems:
    st.markdown("## 결과 요약 📝")
    correct_count = sum(1 for a in st.session_state.answers if a and a.get("correct"))
    total = len(st.session_state.problems)
    st.metric("정답", f"{correct_count} / {total}")

    # 시간 통계
    times = [t for t in st.session_state.times if t is not None]
    if times:
        avg_time = sum(times) / len(times)
        st.write(f"평균 응답 시간: {avg_time:.1f}초")

    # 상세 내역
    with st.expander("문제별 결과 보기"):
        for i, p in enumerate(st.session_state.problems):
            ans = st.session_state.answers[i]
            ok = ans and ans.get("correct")
            status = "✅ 정답" if ok else "❌ 오답"
            given = ans.get("given") if ans else None
            st.write(f"{i+1}. {p['text']} — 정답: {p['answer']} / 입력: {given} — {status}")

    # 재시작 버튼
    if st.button("다시 풀기 ↺"):
        st.session_state.problems = []
        st.session_state.answers = []
        st.session_state.current = 0
        st.session_state.score = 0
        st.session_state.times = []
        st.session_state.start_time = None
        st.session_state.running = False
        st.experimental_rerun()

# 간단한 팁 (항상 보이는 안내)
st.markdown("---")
st.info("팁: 문제를 소리 내어 읽고 큰 자리수부터 빠르게 계산하는 연습을 하세요. 시간을 재서 속도를 점점 단축해보세요.")

# 상태 (디버그용, 필요 없으면 주석 처리 가능)
# st.write(st.session_state)
