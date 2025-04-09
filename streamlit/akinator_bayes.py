import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="아키네이터의 베이즈 정리 기반 추론 과정", layout="wide")

# 제목
st.title("아키네이터의 베이즈 정리 기반 추론 과정 (확장판)")

# 각 단계별 데이터 정의
step_data = [
    {
        "title": "초기 상태",
        "description": "처음에는 모든 인물이 동일한 확률(10%)을 가집니다.",
        "probability_data": pd.DataFrame([
            {"name": '손흥민', "probability": 10},
            {"name": '백종원', "probability": 10},
            {"name": '아이유', "probability": 10},
            {"name": '김연아', "probability": 10},
            {"name": '박지성', "probability": 10},
            {"name": '아이언맨', "probability": 10},
            {"name": '전지현', "probability": 10},
            {"name": '유재석', "probability": 10},
            {"name": '이순신', "probability": 10},
            {"name": '공유', "probability": 10}
        ]),
        "likelihood_table": None,
        "bayes_table": None
    },
    {
        "title": "질문 1: '당신이 생각한 인물은 실존인물인가요?' - 답변: '예'",
        "description": "가상인물(아이언맨)의 확률은 0이 되고, 나머지 인물들의 확률이 재조정됩니다.",
        "probability_data": pd.DataFrame([
            {"name": '손흥민', "probability": 11.1},
            {"name": '백종원', "probability": 11.1},
            {"name": '아이유', "probability": 11.1},
            {"name": '김연아', "probability": 11.1},
            {"name": '박지성', "probability": 11.1},
            {"name": '전지현', "probability": 11.1},
            {"name": '유재석', "probability": 11.1},
            {"name": '이순신', "probability": 11.1},
            {"name": '공유', "probability": 11.1}
        ]),
        "likelihood_table": pd.DataFrame([
            {"name": '손흥민', "value": '실존인물 | 가능도: 100%'},
            {"name": '백종원', "value": '실존인물 | 가능도: 100%'},
            {"name": '아이유', "value": '실존인물 | 가능도: 100%'},
            {"name": '김연아', "value": '실존인물 | 가능도: 100%'},
            {"name": '박지성', "value": '실존인물 | 가능도: 100%'},
            {"name": '아이언맨', "value": '가상인물 | 가능도: 0%'},
            {"name": '전지현', "value": '실존인물 | 가능도: 100%'},
            {"name": '유재석', "value": '실존인물 | 가능도: 100%'},
            {"name": '이순신', "value": '실존인물 | 가능도: 100%'},
            {"name": '공유', "value": '실존인물 | 가능도: 100%'}
        ]),
        "bayes_table": [
            ["단계", "손흥민", "백종원", "아이유", "김연아", "박지성", "아이언맨", "전지현", "유재석", "이순신", "공유"],
            ["사전 확률", "10%", "10%", "10%", "10%", "10%", "10%", "10%", "10%", "10%", "10%"],
            ["가능도", "100%", "100%", "100%", "100%", "100%", "0%", "100%", "100%", "100%", "100%"],
            ["베이즈 분자", "10%", "10%", "10%", "10%", "10%", "0%", "10%", "10%", "10%", "10%"],
            ["정규화 후", "11.1%", "11.1%", "11.1%", "11.1%", "11.1%", "0%", "11.1%", "11.1%", "11.1%", "11.1%"]
        ]
    },
    {
        "title": "질문 2: '당신이 생각한 인물은 남자인가요?' - 답변: '예'",
        "description": "여자 인물들(아이유, 김연아, 전지현)의 확률은 0이 되고, 남은 인물들의 확률이 재조정됩니다.",
        "probability_data": pd.DataFrame([
            {"name": '손흥민', "probability": 20},
            {"name": '백종원', "probability": 20},
            {"name": '박지성', "probability": 20},
            {"name": '유재석', "probability": 20},
            {"name": '이순신', "probability": 20},
            {"name": '공유', "probability": 20}
        ]),
        "likelihood_table": pd.DataFrame([
            {"name": '손흥민', "value": '남자 | 가능도: 100%'},
            {"name": '백종원', "value": '남자 | 가능도: 100%'},
            {"name": '아이유', "value": '여자 | 가능도: 0%'},
            {"name": '김연아', "value": '여자 | 가능도: 0%'},
            {"name": '박지성', "value": '남자 | 가능도: 100%'},
            {"name": '전지현', "value": '여자 | 가능도: 0%'},
            {"name": '유재석', "value": '남자 | 가능도: 100%'},
            {"name": '이순신', "value": '남자 | 가능도: 100%'},
            {"name": '공유', "value": '남자 | 가능도: 100%'}
        ]),
        "bayes_table": [
            ["단계", "손흥민", "백종원", "아이유", "김연아", "박지성", "전지현", "유재석", "이순신", "공유"],
            ["사전 확률", "11.1%", "11.1%", "11.1%", "11.1%", "11.1%", "11.1%", "11.1%", "11.1%", "11.1%"],
            ["가능도", "100%", "100%", "0%", "0%", "100%", "0%", "100%", "100%", "100%"],
            ["베이즈 분자", "11.1%", "11.1%", "0%", "0%", "11.1%", "0%", "11.1%", "11.1%", "11.1%"],
            ["정규화 후", "20%", "20%", "0%", "0%", "20%", "0%", "20%", "20%", "20%"]
        ]
    },
    {
        "title": "질문 3: '당신이 생각한 인물은 40세 이상인가요?' - 답변: '예'",
        "description": "40세 미만 인물들(손흥민, 박지성, 공유)의 확률은 0이 되고, 40세 이상 인물들의 확률이 재조정됩니다.",
        "probability_data": pd.DataFrame([
            {"name": '백종원', "probability": 33.3},
            {"name": '유재석', "probability": 33.3},
            {"name": '이순신', "probability": 33.3}
        ]),
        "likelihood_table": pd.DataFrame([
            {"name": '손흥민', "value": '40세 미만 | 가능도: 0%'},
            {"name": '백종원', "value": '40세 이상 | 가능도: 100%'},
            {"name": '박지성', "value": '40세 미만 | 가능도: 0%'},
            {"name": '유재석', "value": '40세 이상 | 가능도: 100%'},
            {"name": '이순신', "value": '40세 이상 | 가능도: 100%'},
            {"name": '공유', "value": '40세 미만 | 가능도: 0%'}
        ]),
        "bayes_table": [
            ["단계", "손흥민", "백종원", "박지성", "유재석", "이순신", "공유"],
            ["사전 확률", "20%", "20%", "20%", "20%", "20%", "20%"],
            ["가능도", "0%", "100%", "0%", "100%", "100%", "0%"],
            ["베이즈 분자", "0%", "20%", "0%", "20%", "20%", "0%"],
            ["정규화 후", "0%", "33.3%", "0%", "33.3%", "33.3%", "0%"]
        ]
    },
    {
        "title": "질문 4: '당신이 생각한 인물은 요리와 관련이 있나요?' - 답변: '예'",
        "description": "요리와 관련 없는 인물들(유재석, 이순신)의 확률은 0이 되고, 백종원의 확률이 100%가 됩니다.",
        "probability_data": pd.DataFrame([
            {"name": '백종원', "probability": 100}
        ]),
        "likelihood_table": pd.DataFrame([
            {"name": '백종원', "value": '요리 관련 | 가능도: 100%'},
            {"name": '유재석', "value": '요리 무관 | 가능도: 0%'},
            {"name": '이순신', "value": '요리 무관 | 가능도: 0%'}
        ]),
        "bayes_table": [
            ["단계", "백종원", "유재석", "이순신"],
            ["사전 확률", "33.3%", "33.3%", "33.3%"],
            ["가능도", "100%", "0%", "0%"],
            ["베이즈 분자", "33.3%", "0%", "0%"],
            ["정규화 후", "100%", "0%", "0%"]
        ]
    },
    {
        "title": "질문 5: '당신이 생각한 인물은 TV 방송에 자주 출연하나요?' - 답변: '예'",
        "description": "확인 질문으로, 백종원이 정답임을 확정합니다.",
        "probability_data": pd.DataFrame([
            {"name": '백종원', "probability": 100}
        ]),
        "likelihood_table": pd.DataFrame([
            {"name": '백종원', "value": 'TV 출연 다수 | 가능도: 100%'}
        ]),
        "bayes_table": [
            ["단계", "백종원"],
            ["사전 확률", "100%"],
            ["가능도", "100%"],
            ["베이즈 분자", "100%"],
            ["정규화 후", "100%"]
        ]
    }
]

# 확률 변화 트래킹 데이터
probability_tracking = pd.DataFrame([
    {"단계": '초기', "손흥민": 10, "백종원": 10, "아이유": 10, "김연아": 10, "박지성": 10, "아이언맨": 10, "전지현": 10, "유재석": 10, "이순신": 10, "공유": 10},
    {"단계": '질문1', "손흥민": 11.1, "백종원": 11.1, "아이유": 11.1, "김연아": 11.1, "박지성": 11.1, "아이언맨": 0, "전지현": 11.1, "유재석": 11.1, "이순신": 11.1, "공유": 11.1},
    {"단계": '질문2', "손흥민": 20, "백종원": 20, "아이유": 0, "김연아": 0, "박지성": 20, "아이언맨": 0, "전지현": 0, "유재석": 20, "이순신": 20, "공유": 20},
    {"단계": '질문3', "손흥민": 0, "백종원": 33.3, "아이유": 0, "김연아": 0, "박지성": 0, "아이언맨": 0, "전지현": 0, "유재석": 33.3, "이순신": 33.3, "공유": 0},
    {"단계": '질문4', "손흥민": 0, "백종원": 100, "아이유": 0, "김연아": 0, "박지성": 0, "아이언맨": 0, "전지현": 0, "유재석": 0, "이순신": 0, "공유": 0},
    {"단계": '질문5', "손흥민": 0, "백종원": 100, "아이유": 0, "김연아": 0, "박지성": 0, "아이언맨": 0, "전지현": 0, "유재석": 0, "이순신": 0, "공유": 0}
])

# 상위 5개 인물
top_characters = ['백종원', '유재석', '손흥민', '이순신', '박지성']

# 단계 선택 슬라이더
step = st.slider("단계 선택", 0, len(step_data) - 1, 0)

# 현재 단계 데이터
current_data = step_data[step]

# 단계 제목과 설명
st.subheader(current_data["title"])
st.info(current_data["description"])

# 인물 확률 분포 차트
st.subheader("현재 인물 확률 분포")
fig = px.bar(
    current_data["probability_data"], 
    x="name", 
    y="probability", 
    color_discrete_sequence=["#8884d8"],
    labels={"name": "인물", "probability": "확률 (%)"}
)
fig.update_layout(yaxis_range=[0, 100])
st.plotly_chart(fig, use_container_width=True)

# 가능도 테이블
if current_data["likelihood_table"] is not None:
    st.subheader("현재 질문에 대한 가능도 분석")
    st.dataframe(current_data["likelihood_table"], hide_index=True)

# 베이즈 정리 테이블
if current_data["bayes_table"] is not None:
    st.subheader("베이즈 정리 계산 과정")
    bayes_df = pd.DataFrame(current_data["bayes_table"][1:], columns=current_data["bayes_table"][0])
    st.dataframe(bayes_df)

# 확률 변화 트래킹 차트 (상위 5개 인물만)
st.subheader("질문에 따른 확률 변화 추적 (주요 인물)")
tracking_data = probability_tracking.iloc[:step + 2].copy()
line_fig = px.line(
    tracking_data, 
    x="단계", 
    y=top_characters,
    labels={"value": "확률 (%)", "variable": "인물"},
    markers=True
)
line_fig.update_layout(yaxis_range=[0, 100])
st.plotly_chart(line_fig, use_container_width=True)

# 의사결정 과정
st.subheader("질문 의사결정 진행 과정")

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.markdown(f"""
    <div style="background-color: {'#cceeff' if step >= 0 else '#f0f0f0'}; padding: 10px; border-radius: 5px; text-align: center;">
        <strong>초기 상태</strong><br>
        <small>10명의 인물, 각 10%</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color: {'#cceeff' if step >= 1 else '#f0f0f0'}; padding: 10px; border-radius: 5px; text-align: center;">
        <strong>질문 1</strong><br>
        <small>실존인물? (남은 인물: 9명)</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background-color: {'#cceeff' if step >= 2 else '#f0f0f0'}; padding: 10px; border-radius: 5px; text-align: center;">
        <strong>질문 2</strong><br>
        <small>남자? (남은 인물: 6명)</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background-color: {'#cceeff' if step >= 3 else '#f0f0f0'}; padding: 10px; border-radius: 5px; text-align: center;">
        <strong>질문 3</strong><br>
        <small>40세 이상? (남은 인물: 3명)</small>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div style="background-color: {'#cceeff' if step >= 4 else '#f0f0f0'}; padding: 10px; border-radius: 5px; text-align: center;">
        <strong>질문 4</strong><br>
        <small>요리 관련? (남은 인물: 1명)</small>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div style="background-color: {'#cceeff' if step >= 5 else '#f0f0f0'}; padding: 10px; border-radius: 5px; text-align: center;">
        <strong>질문 5</strong><br>
        <small>TV 출연? (정답: 백종원)</small>
    </div>
    """, unsafe_allow_html=True)

# 마지막 단계일 경우 결론 표시
if step == len(step_data) - 1:
    st.success("""
    ## 결론
    다섯 번의 질문을 통해 아키네이터는 "백종원"이라는 정답을 찾아냈습니다! 
    이것이 베이즈 정리의 강력함입니다. 각 질문마다 새로운 정보를 반영하여 확률을 업데이트하고,
    가능성이 낮은 인물들을 제거해 나가면서 정답에 도달했습니다.
    실제 아키네이터는 수천 개의 인물과 수백 개의 특성을 고려하는 훨씬 더 복잡한 베이즈 추론을 수행합니다.
    """) 