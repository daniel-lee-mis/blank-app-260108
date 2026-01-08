# 🧮 암산 챌린지 (초등 5학년)

간단하고 빠르게 반복 학습하는 암산 연습용 웹앱입니다. 이 저장소에는 초등 5학년 수준의 연산 문제(덧셈/뺄셈/곱셈/나눗셈)를 자동으로 생성하고, 각 문제를 풀고 제출하면 채점·기록·요약을 제공하는 Streamlit 앱이 포함되어 있습니다.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

## 🔧 실행 방법 (로컬)

1. 의존성 설치

```bash
pip install -r requirements.txt
```

2. 앱 실행

```bash
streamlit run streamlit_app.py
```

3. 브라우저에서 열기: 기본적으로 http://localhost:8501 에서 확인할 수 있습니다.

> 팁: 가상환경(venv/conda)을 사용하는 것을 권장합니다.

## 🧭 사용 안내

1. 사이드바에서 난이도와 연산 유형, 문제 수, 타이머 사용 여부를 설정합니다.
2. **"새로운 세션 시작 🚀"** 버튼을 누르면 문제들이 생성됩니다.
3. 각 문제에 대해 암산으로 정답을 계산하고 **정답 입력 → 제출** 합니다.
4. 제출 후 정답/오답이 표시되며, 세션이 끝나면 요약 결과를 확인할 수 있습니다.
5. 필요하면 **"포기하고 답 보기 ❌"** 로 정답을 확인하고 다음 문제로 넘어가세요.
