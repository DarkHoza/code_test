#####################################
# PART 1
#####################################

import streamlit as st
st.set_page_config(page_title="Selectbox + Tabs + Columns + Google Sheets(OAuth)", layout="wide")


import pandas as pd
import plotly.express as px
import itertools
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import datetime
import numpy as np
from utils import hide_sidebar_pages
import page.page_category as page_category

# OAuth 관련 라이브러리
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

#####################################
# 1) 세션 상태 키 초기화 (카테고리별 매출 토글용)
#####################################
if "show_category" not in st.session_state:
    st.session_state["show_category"] = False

#####################################
# 2) 금액 단위 표시 함수 추가 (조 단위 지원)
#####################################
def format_currency(amount):
    """
    금액을 조 단위 또는 억 단위로 표시
    예: 11219억 -> 1조 1,219억
    """
    if amount >= 10000:  # 10000억 = 1조
        jo = amount // 10000
        eok = amount % 10000
        if eok > 0:
            return f"{jo}조 {eok:,}억"
        else:
            return f"{jo}조"
    else:
        return f"{amount:,}억"

# 구글 시트 데이터를 캐싱하는 함수 수정
@st.cache_data(ttl=3600)  # 1시간마다 갱신
def load_category_sheet_data(sheet_url, sheet_name, _client):
    try:
        ws = _client.open_by_key(sheet_url).worksheet(sheet_name)
        data = ws.get_all_values()
        
        if len(data) >= 2:
            header = data[0]
            rows = data[1:]
            df = pd.DataFrame(rows, columns=header)
            
            # 숫자형 데이터 변환 (첫 번째 열은 날짜/기간 열이므로 제외)
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
        else:
            return None
    except Exception as e:
        print(f"시트 데이터 로드 오류: {e}")
        return None
#####################################
# 3) 메인 화면 제목 / 스타일
#####################################
st.title("종합 대시보드")
st.markdown("비즈니스컨설팅팀 각 주제별 대시보드를 확인하세요.")

# 추가 스타일
st.markdown("""
<style>
.modern-card {
    background-color: #f0f8ff;
    border-radius: 15px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.25);
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    text-align: center;
}
.modern-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px rgba(0,0,0,0.15);
}
.modern-card h4 {
    font-size: 22px;
    color: #222;
    margin-bottom: 10px;
    font-weight: 600;
    text-align: center;
}
.modern-card .value {
    font-size: 36px;
    font-weight: bold;
    color: #333;
    margin-bottom: 14px;
    text-align: center;
}
.badge {
    display: inline-block;
    padding: 6px 13px;
    border-radius: 15px;
    color: #fff;
    font-size: 14px;
    margin: 2px;
}
.badge.blue {
    background-color: #3b82f6;
}
.badge.green {
    background-color: #10b981;
}
.badge.red {
    background-color: #ef4444;
}
</style>
""", unsafe_allow_html=True)

#####################################
# 4) 사이드바에서 Topic 선택
#####################################
topic = st.sidebar.selectbox(
    "주제 선택",
    ["종합 대시보드", "Data-eye 대시보드", "Topic A", "Topic B", "Topic C"]
)
# ---------------------------------------
# Topic A
# ---------------------------------------
if topic == "Topic A":
    st.header("Topic A 대시보드")
    st.markdown("Topic A 관련 주요 지표와 차트입니다.")

    tabs_A = st.tabs(["A1", "A2"])

    # A1 탭
    with tabs_A[0]:
        st.subheader("A1 탭")
        col1, col2 = st.columns(2)
        with col1:
            df_a1 = pd.DataFrame({
                "Category": ["A1-cat1", "A1-cat2", "A1-cat3"],
                "Value": [10, 15, 8]
            })
            fig_a1 = px.bar(df_a1, x="Category", y="Value", title="Bar Chart A1")
            st.plotly_chart(fig_a1, use_container_width=True)
        with col2:
            df_a2 = pd.DataFrame({
                "Category": ["A1-cat1", "A1-cat2", "A1-cat3"],
                "Value": [12, 18, 10]
            })
            fig_a2 = px.line(df_a2, x="Category", y="Value", title="Line Chart A1")
            st.plotly_chart(fig_a2, use_container_width=True)

    # A2 탭
    with tabs_A[1]:
        st.subheader("A2 탭")
        col1, col2 = st.columns(2)
        with col1:
            df_a3 = pd.DataFrame({
                "Category": ["A2-cat1", "A2-cat2", "A2-cat3"],
                "Value": [20, 25, 30]
            })
            fig_a3 = px.pie(df_a3, names="Category", values="Value", title="Pie Chart A2")
            st.plotly_chart(fig_a3, use_container_width=True)
        with col2:
            df_a4 = pd.DataFrame({
                "Category": ["A2-cat1", "A2-cat2", "A2-cat3"],
                "Value": [30, 20, 10]
            })
            fig_a4 = px.scatter(df_a4, x="Category", y="Value", title="Scatter Chart A2")
            st.plotly_chart(fig_a4, use_container_width=True)

# ---------------------------------------
# Topic B
# ---------------------------------------
elif topic == "Topic B":
    st.header("Topic B 대시보드")
    st.markdown("Topic B 관련 주요 지표와 차트입니다.")

    tabs_B = st.tabs(["B1", "B2"])

    # B1 탭
    with tabs_B[0]:
        st.subheader("B1 탭")
        col1, col2 = st.columns(2)
        with col1:
            df_b1 = pd.DataFrame({
                "Month": ["Jan", "Feb", "Mar"],
                "Sales": [100, 150, 200]
            })
            fig_b1 = px.bar(df_b1, x="Month", y="Sales", title="Bar Chart B1")
            st.plotly_chart(fig_b1, use_container_width=True)
        with col2:
            df_b2 = pd.DataFrame({
                "Month": ["Jan", "Feb", "Mar"],
                "Sales": [120, 160, 210]
            })
            fig_b2 = px.line(df_b2, x="Month", y="Sales", title="Line Chart B1")
            st.plotly_chart(fig_b2, use_container_width=True)

    # B2 탭
    with tabs_B[1]:
        st.subheader("B2 탭")
        col1, col2 = st.columns(2)
        with col1:
            df_b3 = pd.DataFrame({
                "Product": ["Prod A", "Prod B", "Prod C"],
                "Value": [50, 70, 60]
            })
            fig_b3 = px.pie(df_b3, names="Product", values="Value", title="Pie Chart B2")
            st.plotly_chart(fig_b3, use_container_width=True)
        with col2:
            df_b4 = pd.DataFrame({
                "Product": ["Prod A", "Prod B", "Prod C"],
                "Value": [55, 65, 75]
            })
            fig_b4 = px.scatter(df_b4, x="Product", y="Value", title="Scatter Chart B2")
            st.plotly_chart(fig_b4, use_container_width=True)
            # ---------------------------------------
# Topic C
# ---------------------------------------
elif topic == "Topic C":
    st.header("Topic C 대시보드")
    st.markdown("Topic C를 4개 탭(C1, C2, C3, C4)으로 구분합니다.")

    tabs_C = st.tabs(["C1", "C2", "C3", "C4"])

    link_url = "https://docs.google.com/spreadsheets/d/1KWnrxOMRhRJlT2lnFKwrl-3r9eJBMeArhJuB-nI7OMU/edit?gid=1787054277#gid=1787054277"

    # C1
    with tabs_C[0]:
        st.subheader("C1: columns 이용 사이트맵 (링크 포함)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                "#### 교육\n- <a href='{}' target='_blank'>사전교육</a>\n- <a href='{}' target='_blank'>실습자료</a>\n- <a href='{}' target='_blank'>Q&A 세션</a>".format(
                    link_url, link_url, link_url),
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                "#### 배경\n- <a href='{}' target='_blank'>추진배경</a>\n- <a href='{}' target='_blank'>시장현황</a>\n- <a href='{}' target='_blank'>경쟁사분석</a>".format(
                    link_url, link_url, link_url),
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                "#### 목표\n- <a href='{}' target='_blank'>매출증대</a>\n- <a href='{}' target='_blank'>고객확보</a>\n- <a href='{}' target='_blank'>점유율 상승</a>".format(
                    link_url, link_url, link_url),
                unsafe_allow_html=True
            )

    # C2
    with tabs_C[1]:
        st.subheader("C2: columns 이용 사이트맵 (4열, 링크 포함)")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                "#### 요약\n- <a href='{}' target='_blank'>프로젝트 요약</a>\n- <a href='{}' target='_blank'>일정</a>\n- <a href='{}' target='_blank'>위험요소</a>".format(
                    link_url, link_url, link_url),
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                "#### DB 관련\n- <a href='{}' target='_blank'>DB 구조</a>\n- <a href='{}' target='_blank'>쿼리 예시</a>\n- <a href='{}' target='_blank'>인덱스 전략</a>".format(
                    link_url, link_url, link_url),
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                "#### 운영\n- <a href='{}' target='_blank'>운영 가이드</a>\n- <a href='{}' target='_blank'>서버 구성</a>\n- <a href='{}' target='_blank'>모니터링</a>".format(
                    link_url, link_url, link_url),
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                "#### 기타\n- <a href='{}' target='_blank'>지원</a>\n- <a href='{}' target='_blank'>문서</a>\n- <a href='{}' target='_blank'>참고자료</a>".format(
                    link_url, link_url, link_url),
                unsafe_allow_html=True
            )

    # C3
    with tabs_C[2]:
        st.subheader("C3: HTML 테이블 사이트맵 1 (링크 포함)")
        custom_css = """
        <style>
        .sitemap-table {
        width: 100%;
        border-collapse: collapse;
        }
        .sitemap-table th, .sitemap-table td {
        border: 1px solid #ddd;
        padding: 8px;
        vertical-align: top;
        }
        .sitemap-table th {
        background-color: #f2f2f2;
        text-align: center;
        }
        .sitemap-table tr:hover {background-color: #f9f9f9;}
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)

        html_table_c3 = f"""
        <table class="sitemap-table">
          <tr>
            <th><a href="{link_url}" target="_blank">항목</a></th>
            <th><a href="{link_url}" target="_blank">설명</a></th>
            <th><a href="{link_url}" target="_blank">비고</a></th>
          </tr>
          <tr>
            <td><a href="{link_url}" target="_blank">교육</a></td>
            <td><a href="{link_url}" target="_blank">사전교육, 실습자료, Q&amp;A 세션</a></td>
            <td><a href="{link_url}" target="_blank">필수 이수</a></td>
          </tr>
          <tr>
            <td><a href="{link_url}" target="_blank">배경</a></td>
            <td><a href="{link_url}" target="_blank">추진배경, 시장현황, 경쟁사분석</a></td>
            <td><a href="{link_url}" target="_blank">리서치 완료</a></td>
          </tr>
          <tr>
            <td><a href="{link_url}" target="_blank">목표</a></td>
            <td><a href="{link_url}" target="_blank">매출증대, 고객확보, 점유율 상승</a></td>
            <td><a href="{link_url}" target="_blank">전사 공감대</a></td>
          </tr>
        </table>
        """
        st.markdown(html_table_c3, unsafe_allow_html=True)

    # C4
    with tabs_C[3]:
        st.subheader("C4: HTML 테이블 사이트맵 2 (4열, 링크 포함)")
        custom_css2 = """
        <style>
        .sitemap-table2 {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        }
        .sitemap-table2 th, .sitemap-table2 td {
        border: 1px solid #aaa;
        padding: 8px;
        vertical-align: top;
        }
        .sitemap-table2 th {
        background-color: #e0e0e0;
        text-align: center;
        }
        .sitemap-table2 tr:hover {background-color: #fafafa;}
        </style>
        """
        st.markdown(custom_css2, unsafe_allow_html=True)

        html_table_c4 = f"""
        <table class="sitemap-table2">
          <tr>
            <th><a href="{link_url}" target="_blank">구분</a></th>
            <th><a href="{link_url}" target="_blank">내용</a></th>
            <th><a href="{link_url}" target="_blank">진행상태</a></th>
            <th><a href="{link_url}" target="_blank">비고</a></th>
          </tr>
          <tr>
            <td><a href="{link_url}" target="_blank">DB 관련</a></td>
            <td><a href="{link_url}" target="_blank">DB 구조, 쿼리 예시, 인덱스 전략</a></td>
            <td><a href="{link_url}" target="_blank">진행중</a></td>
            <td><a href="{link_url}" target="_blank">확인 필요</a></td>
          </tr>
          <tr>
            <td><a href="{link_url}" target="_blank">운영</a></td>
            <td><a href="{link_url}" target="_blank">운영 가이드, 서버 구성, 모니터링</a></td>
            <td><a href="{link_url}" target="_blank">완료</a></td>
            <td><a href="{link_url}" target="_blank">문서 정리</a></td>
          </tr>
          <tr>
            <td><a href="{link_url}" target="_blank">기타</a></td>
            <td><a href="{link_url}" target="_blank">지원, 문서, 참고자료</a></td>
            <td><a href="{link_url}" target="_blank">대기</a></td>
            <td><a href="{link_url}" target="_blank">추가 요청</a></td>
          </tr>
        </table>
        """
        st.markdown(html_table_c4, unsafe_allow_html=True)
        # ---------------------------------------
# 구글 시트 데이터 (Topic D - 종합 대시보드)
# ---------------------------------------
elif topic == "종합 대시보드":
    # 탭 구성 - 디지털트윈 탭 추가
    tabs_D = st.tabs(["타사이전 지표", "TOP100 / VIP 관리몰", "카테고리별 매출", "카페24 EC 전체", "디지털트윈"])

    # 1) OAuth 범위 지정
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = None

    # 2) 기존에 토큰이 있다면 불러와 재사용
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # 3) 만료됐거나 없으면 새로 로그인
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 토큰이 만료됐지만 refresh_token이 있을 때
            creds.refresh(Request())
        else:
            # 처음 인증할 때
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # 로그인 완료 후 토큰 저장
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # 데이터프레임 및 변수 기본값 초기화
    df = pd.DataFrame()
    df_sales = None
    df_ec_category = None
    df_mall_category = None

    # 4) gspread 인증 및 데이터 로드
    try:
        client = gspread.authorize(creds)

        # 스프레드시트 열기
        sheet_url = "1o1tptX_-9NEoitHwUTh-OZSqRTdqysSEgMcl6_JNSzY"  # 구글 스프레드시트 key
        sheet_name = "[통합검색]업체정보"
        sh = client.open_by_key(sheet_url)
        ws = sh.worksheet(sheet_name)

        # 데이터 불러오기
        data = ws.get_all_values()
        
        # 카테고리 데이터 로드
        try:
            # 시트 URL 정의
            sales_sheet_url = "1hrpu7fL5b7zQnwGwLTfq5tx3WtNJ-ZTeEiVWGhzbkx4"
            
            # EC전체 카테고리 및 관리몰 카테고리 시트 불러오기
            df_ec_category = load_category_sheet_data(sales_sheet_url, "EC전체 카테고리", client)
            df_mall_category = load_category_sheet_data(sales_sheet_url, "관리몰 카테고리", client)
            
            # 데이터프레임을 세션 상태에 저장
            if df_ec_category is not None:
                st.session_state['df_ec_category'] = df_ec_category
                print(f"EC전체 카테고리 데이터 로드 완료: {len(df_ec_category)}행, {len(df_ec_category.columns)}열")
            
            if df_mall_category is not None:
                st.session_state['df_mall_category'] = df_mall_category
                print(f"관리몰 카테고리 데이터 로드 완료: {len(df_mall_category)}행, {len(df_mall_category.columns)}열")
            
        except Exception as e:
            st.error(f"카테고리 데이터를 불러오는 중 오류가 발생했습니다: {e}")
            import traceback
            print(traceback.format_exc())
            
        if len(data) < 3:
            st.warning("시트에 데이터가 충분히 없습니다.")
            df = pd.DataFrame()  # 빈 데이터프레임 생성
        else:
            # 추가 스프레드시트 열기
            sales_sheet_url = "1hrpu7fL5b7zQnwGwLTfq5tx3WtNJ-ZTeEiVWGhzbkx4"  # 매출 스프레드시트 key
            sales_sheet_name = "매출"
            sales_sh = client.open_by_key(sales_sheet_url)
            sales_ws = sales_sh.worksheet(sales_sheet_name)

            # 매출 데이터 불러오기
            sales_data = sales_ws.get_all_values()

            if len(sales_data) >= 2:
                # 헤더 처리 (1행이 헤더)
                sales_header = sales_data[0]  # ['해당월', 'VIP', 'TOP100', '전체']
                sales_rows = sales_data[1:]

                # 데이터프레임 생성
                df_sales = pd.DataFrame(sales_rows, columns=sales_header)

                # 숫자 컬럼 변환
                for col in ['VIP', 'TOP100', '전체']:
                    df_sales[col] = pd.to_numeric(df_sales[col], errors='coerce')

                # 데이터프레임을 세션 상태에 저장
                st.session_state['df_sales'] = df_sales
            else:
                st.warning("매출 시트에 데이터가 충분히 없습니다.")
                df_sales = None

            # 중복 컬럼명 처리 로직
            header = data[1]
            rows = data[2:]
            max_columns = max(len(row) for row in rows)
            if len(header) < max_columns:
                header.extend([""] * (max_columns - len(header)))
            new_header = []
            counts = {}
            for col in header:
                if col not in counts:
                    counts[col] = 1
                    new_header.append(col)
                else:
                    counts[col] += 1
                    new_header.append(f"{col}_{counts[col]}")

            df = pd.DataFrame(rows, columns=new_header)
    except Exception as e:
        st.error(f"Google Sheets 데이터를 불러오는 중 오류가 발생했습니다: {e}")
        st.write("오류가 발생했습니다. 자세한 내용:", e)
        ###################################
    # 탭 D[0]: 타사이전 지표
    ###################################
    with tabs_D[0]:
        if not df.empty:
            # 날짜 변환 후 추가 (기존 코드 유지)
            df["접수일_dt"] = pd.to_datetime(df["타사이전(접수일)"], format="%y-%m-%d", errors="coerce")
            df["YearMonth"] = df["접수일_dt"].dt.strftime('%Y-%m')

            # 월별 차트 (선택한 기간 전체를 연월 단위로 표시)
            date_range = pd.date_range(start='2022-01-01', end=pd.Timestamp.now(), freq='MS')
            year_month_options = date_range.strftime('%Y-%m').tolist()

            col1, col2, col3 = st.columns([2, 2, 4])

            with col3:
                quick_options = st.radio(
                    "", ["직접 선택", "최근 1개월", "최근 3개월", "최근 6개월", "최근 1년"],
                    horizontal=True, key="quick_period_select"
                )

            today = pd.Timestamp.now().normalize()

            if quick_options == "직접 선택":
                default_start = (today - pd.DateOffset(years=1)).strftime('%Y-01')
                default_end = (today - pd.DateOffset(years=1)).strftime('%Y-12')

                start_index = year_month_options.index(default_start) if default_start in year_month_options else 0
                end_index = year_month_options.index(default_end) if default_end in year_month_options else len(year_month_options) - 1

                with col1:
                    start_period = st.selectbox("시작 연월 선택", year_month_options, index=start_index, key="start_period_select1")
                with col2:
                    end_period = st.selectbox("종료 연월 선택", year_month_options, index=end_index, key="end_period_select1")
            else:
                end_date = today
                if quick_options == "최근 1개월":
                    start_date = (end_date - pd.DateOffset(months=1)).replace(day=1)
                elif quick_options == "최근 3개월":
                    start_date = (end_date - pd.DateOffset(months=3)).replace(day=1)
                elif quick_options == "최근 6개월":
                    start_date = (end_date - pd.DateOffset(months=6)).replace(day=1)
                elif quick_options == "최근 1년":
                    start_date = (end_date - pd.DateOffset(years=1)).replace(day=1)

                start_period = start_date.strftime('%Y-%m')
                end_period = end_date.strftime('%Y-%m')

                with col1:
                    st.markdown(f"**선택기간:** {start_period} ~ {end_period}")

            # 날짜 필터링
            start_date = pd.Timestamp(start_period + '-01')
            end_date = pd.Timestamp(end_period + '-01') + pd.offsets.MonthEnd(1)

            df_filtered = df[(df["접수일_dt"] >= start_date) & (df["접수일_dt"] <= end_date)]

# 카드 데이터 계산
            count_타사이전_이슈 = df_filtered["타사이전(접수일)"].fillna("").str.strip().ne("").sum()
            count_방어중 = (df_filtered["타사이전(현황)"] == "방어중").sum()
            count_타사이전_제외사유 = df_filtered["타사이전(현황)"].fillna("").str.strip().ne("").sum()
            count_이전확정 = (df_filtered["타사이전(현황)"] == "이전확정").sum()
            count_이전완료 = (df_filtered["타사이전(현황)"] == "이전완료").sum()

            st.markdown("""
                <style>
                .section-title {
                    font-size: 20px;
                    font-weight: bold;
                    color: #4B2EA4;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }
                .metric-row {
                    display: flex;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                .metric-card {
                    flex: 1;
                    background: #FFFFFF;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 20px;
                    text-align: center;
                }
                .metric-title {
                    font-size: 14px;
                    color: #777;
                    margin-bottom: 5px;
                }
                .metric-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #4B2EA4;
                }
                </style>
                """, unsafe_allow_html=True)

            # 카드와 차트 영역 분리
            col_left, col_right = st.columns([3, 2])

            with col_left:
                st.markdown('<div class="section-title">타사이전 집계현황</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-card"><div class="metric-title">총 발생수</div><div class="metric-value">{count_타사이전_이슈}</div></div>
                    <div class="metric-card"><div class="metric-title">방어중</div><div class="metric-value">{count_방어중}</div></div>
                    <div class="metric-card"><div class="metric-title">KPI제외</div><div class="metric-value">{count_타사이전_제외사유}</div></div>
                    <div class="metric-card"><div class="metric-title">이전확정</div><div class="metric-value">{count_이전확정}</div></div>
                    <div class="metric-card"><div class="metric-title">이전완료</div><div class="metric-value">{count_이전완료}</div></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="section-title">타사이전 주요사유</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="metric-row">
                    <div class="metric-card"><div class="metric-title">PG수수료 인하</div><div class="metric-value">2</div></div>
                    <div class="metric-card"><div class="metric-title">경영진 영업활동</div><div class="metric-value">2</div></div>
                    <div class="metric-card"><div class="metric-title">기능커스텀 구현불가</div><div class="metric-value">1</div></div>
                    <div class="metric-card"><div class="metric-title">기타</div><div class="metric-value">1</div></div>
                </div>
                """, unsafe_allow_html=True)

                # 월별 차트
                full_month_range = pd.date_range(start=start_date, end=end_date, freq='MS').strftime('%Y-%m')
                df_all_months = pd.DataFrame({'YearMonth': full_month_range})
                df_month_counts = df_filtered.groupby('YearMonth').size().reset_index(name='건수')
                df_monthly_final = pd.merge(df_all_months, df_month_counts, how='left', on='YearMonth').fillna(0)

                fig_bar = px.bar(
                    df_monthly_final,
                    x='YearMonth',
                    y='건수',
                    labels={'YearMonth': '연월', '건수': '건수'},
                    title='기간별 월별 현황'
                )
                fig_bar.update_xaxes(type='category')
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_right:
                st.markdown('<div class="section-title">물구분 비율</div>', unsafe_allow_html=True)
                pie_df1 = pd.DataFrame({
                    "구분": ["국내", "해외(영문,일문)"],
                    "수량": [4, 2]
                })
                fig1 = px.pie(pie_df1, names='구분', values='수량', hole=0.4)
                st.plotly_chart(fig1, use_container_width=True)

                st.markdown('<div class="section-title">카테고리 분포</div>', unsafe_allow_html=True)
                pie_df2 = pd.DataFrame({
                    "카테고리": ["패션", "생활/건강", "화장품", "패션잡화", "출산/육아", "종합"],
                    "수량": [1, 1, 1, 1, 1, 1]
                })
                fig2 = px.pie(pie_df2, names='카테고리', values='수량', hole=0.5)
                st.plotly_chart(fig2, use_container_width=True)

            st.write("#### 스프레드시트 데이터 미리보기")
            st.dataframe(df_filtered)
        else:
            st.warning("타사이전 지표 데이터를 불러올 수 없습니다.")

    ###################################
    # 탭 D[1]: TOP100 / VIP 관리몰
    ###################################
    with tabs_D[1]:
        st.subheader("TOP100 / VIP 관리몰")

        if 'df_sales' in st.session_state and not st.session_state['df_sales'].empty:
            df_sales = st.session_state['df_sales']
            # (1) 최신 월 데이터
            latest_data = df_sales.iloc[-1]
            # (2) 바로 이전 월 데이터
            prev_month_data = df_sales.iloc[-2] if len(df_sales) > 1 else None
            # (3) 작년 동월 데이터
            last_year_same_month = df_sales.iloc[-13] if len(df_sales) > 12 else None
            # 최신 데이터에서 '해당월' 추출
            ref_date = latest_data['해당월']  # 예: "2025-02"
            ref_year, ref_month = ref_date.split("-")
            ref_date_str = f"{ref_year}년 {ref_month}월 기준"

            st.markdown(f"**데이터 기준: {ref_date_str}**")

            # ▼▼▼ 여기서부터 버튼 두 개를 나란히 배치 ▼▼▼
            col_txt, col_spacer, col_btn1, col_btn2 = st.columns([4.5, 4, 1.1, 1])
            
            with col_btn1:
                # (1) 실제 동작하는 토글 버튼
                if st.button("카테고리별 매출"):
                    st.session_state["show_category"] = not st.session_state["show_category"]

            with col_btn2:
                # (2) 원본데이터 버튼 (자바스크립트로 새 탭 열기)
                if st.button("원본데이터"):
                    js_code = f"window.open('https://www.example.com')"
                    st.markdown(f"<script>{js_code}</script>", unsafe_allow_html=True)
                    # ▲▲▲ 버튼 두 개 나란히 배치 끝 ▲▲▲

            # 작년 동월 데이터 (인덱스 -12, 없을 수 있음)
            last_year_same_month = None
            if len(df_sales) > 12:
                last_year_same_month = df_sales.iloc[-13]
            # 카드 섹션 (관리몰 전체 매출, TOP100, VIP)
            col1, col2, col3 = st.columns(3)

            # -----------------------------------------
            # 1) 관리몰 전체 매출
            # -----------------------------------------
            with col1:
                total_revenue = float(latest_data['VIP']) + float(latest_data['TOP100'])
                prev_month_change = 0
                prev_month_percent = 0
                if prev_month_data is not None:
                    prev_month_total = float(prev_month_data['VIP']) + float(prev_month_data['TOP100'])
                    prev_month_change = total_revenue - prev_month_total
                    prev_month_percent = (prev_month_change / prev_month_total * 100) if prev_month_total != 0 else 0

                last_year_change = 0
                last_year_percent = 0
                if last_year_same_month is not None:
                    last_year_total = float(last_year_same_month['VIP']) + float(last_year_same_month['TOP100'])
                    last_year_change = total_revenue - last_year_total
                    last_year_percent = (last_year_change / last_year_total * 100) if last_year_total != 0 else 0

                prev_month_arrow = "▲" if prev_month_change >= 0 else "▼"
                prev_month_badge = "blue" if prev_month_change >= 0 else "green"
                last_year_arrow = "▲" if last_year_change >= 0 else "▼"
                last_year_badge = "blue" if last_year_change >= 0 else "green"

                total_revenue_display = format_currency(int(total_revenue / 100000000))
                prev_month_change_display = format_currency(int(abs(prev_month_change) / 100000000))
                last_year_change_display = format_currency(int(abs(last_year_change) / 100000000))

                st.markdown(f"""
                <div class="modern-card">
                    <h4>관리몰 전체 매출</h4>
                    <div class="value">{total_revenue_display}</div>
                    <div class="badge {prev_month_badge}">{prev_month_arrow} 전월 대비 {prev_month_percent:.1f}%({prev_month_change_display})</div>
                    <div class="badge {last_year_badge}">{last_year_arrow} 전년 대비 {last_year_percent:.1f}%({last_year_change_display})</div>
                </div>
                """, unsafe_allow_html=True)

            # -----------------------------------------
            # 2) TOP100 매출
            # -----------------------------------------
            with col2:
                top100_revenue = float(latest_data['TOP100'])
                top100_prev_month_change = 0
                top100_prev_month_percent = 0
                if prev_month_data is not None:
                    top100_prev_month = float(prev_month_data['TOP100'])
                    top100_prev_month_change = top100_revenue - top100_prev_month
                    top100_prev_month_percent = (top100_prev_month_change / top100_prev_month * 100) if top100_prev_month != 0 else 0

                top100_last_year_change = 0
                top100_last_year_percent = 0
                if last_year_same_month is not None:
                    top100_last_year = float(last_year_same_month['TOP100'])
                    top100_last_year_change = top100_revenue - top100_last_year
                    top100_last_year_percent = (top100_last_year_change / top100_last_year * 100) if top100_last_year != 0 else 0

                top100_prev_arrow = "▲" if top100_prev_month_change >= 0 else "▼"
                top100_prev_badge = "blue" if top100_prev_month_change >= 0 else "green"
                top100_last_year_arrow = "▲" if top100_last_year_change >= 0 else "▼"
                top100_last_year_badge = "blue" if top100_last_year_change >= 0 else "green"

                top100_revenue_display = format_currency(int(top100_revenue / 100000000))
                top100_prev_month_change_display = format_currency(int(abs(top100_prev_month_change) / 100000000))
                top100_last_year_change_display = format_currency(int(abs(top100_last_year_change) / 100000000))

                st.markdown(f"""
                <div class="modern-card">
                    <h4>TOP100</h4>
                    <div class="value">{top100_revenue_display}</div>
                    <div class="badge {top100_prev_badge}">{top100_prev_arrow} 전월 대비 {top100_prev_month_percent:.1f}%({top100_prev_month_change_display})</div>
                    <div class="badge {top100_last_year_badge}">{top100_last_year_arrow} 전년 대비 {top100_last_year_percent:.1f}%({top100_last_year_change_display})</div>
                </div>
                """, unsafe_allow_html=True)

            # -----------------------------------------
            # 3) VIP 매출
            # -----------------------------------------
            with col3:
                vip_revenue = float(latest_data['VIP'])
                vip_prev_month_change = 0
                vip_prev_month_percent = 0
                if prev_month_data is not None:
                    vip_prev_month = float(prev_month_data['VIP'])
                    vip_prev_month_change = vip_revenue - vip_prev_month
                    vip_prev_month_percent = (vip_prev_month_change / vip_prev_month * 100) if vip_prev_month != 0 else 0

                vip_last_year_change = 0
                vip_last_year_percent = 0
                if last_year_same_month is not None:
                    vip_last_year = float(last_year_same_month['VIP'])
                    vip_last_year_change = vip_revenue - vip_last_year
                    vip_last_year_percent = (vip_last_year_change / vip_last_year * 100) if vip_last_year != 0 else 0

                vip_prev_arrow = "▲" if vip_prev_month_change >= 0 else "▼"
                vip_prev_badge = "blue" if vip_prev_month_change >= 0 else "green"
                vip_last_year_arrow = "▲" if vip_last_year_change >= 0 else "▼"
                vip_last_year_badge = "blue" if vip_last_year_change >= 0 else "green"

                vip_revenue_display = format_currency(int(vip_revenue / 100000000))
                vip_prev_month_change_display = format_currency(int(abs(vip_prev_month_change) / 100000000))
                vip_last_year_change_display = format_currency(int(abs(vip_last_year_change) / 100000000))

                st.markdown(f"""
                <div class="modern-card">
                    <h4>VIP</h4>
                    <div class="value">{vip_revenue_display}</div>
                    <div class="badge {vip_prev_badge}">{vip_prev_arrow} 전월 대비 {vip_prev_month_percent:.1f}%({vip_prev_month_change_display})</div>
                    <div class="badge {vip_last_year_badge}">{last_year_arrow} 전년 대비 {last_year_percent:.1f}%({last_year_change_display})</div>
                </div>
                """, unsafe_allow_html=True)
            with st.expander("월별 매출 원본 데이터", expanded=True):
                df_display = df_sales[['해당월', 'VIP', 'TOP100']].copy()
                df_display['VIP'] = df_display['VIP'].apply(lambda x: format_currency(int(x/100000000)) if pd.notnull(x) else "")
                df_display['TOP100'] = df_display['TOP100'].apply(lambda x: format_currency(int(x/100000000)) if pd.notnull(x) else "")
                st.dataframe(df_display)

            with st.expander("📊 월간 분석(샘플)", expanded=True):
                st.markdown("""
                - 지난달 대비 VIP 매출 증가율 2.4%
                - TOP100 신규 진입 브랜드 5개
                - 이커머스 트렌드: AI 활용 마케팅 증가
                - 특정 카테고리(패션/리빙) 성장세 지속
                """)


            # 라인 차트 (연도+지표별)
            df_chart = df_sales.copy()
            df_chart['VIP'] = df_chart['VIP'] / 100_000_000
            df_chart['TOP100'] = df_chart['TOP100'] / 100_000_000

            df_chart['해당월_dt'] = pd.to_datetime(df_chart['해당월'], errors='coerce')
            df_chart.dropna(subset=['해당월_dt'], inplace=True)
            df_chart['Year'] = df_chart['해당월_dt'].dt.year
            df_chart['Month'] = df_chart['해당월_dt'].dt.month

            df_filtered = df_chart[df_chart['Year'].isin([2024, 2025])]

            df_melted = df_filtered.melt(
                id_vars=['Year', 'Month'],
                value_vars=['VIP', 'TOP100'],
                var_name='Metric',
                value_name='Value'
            )
            df_melted['Year_Metric'] = df_melted['Year'].astype(str) + '_' + df_melted['Metric']

            fig = px.line(
                df_melted,
                x='Month',
                y='Value',
                color='Year_Metric',
                markers=True,
                labels={'Month': '월', 'Value': '매출(억 원)'},
                title="TOP100 / VIP 관리몰 월별 매출 (연도+지표별)",
                color_discrete_map={
                    "2024_VIP": "rgba(255,165,0,0.3)",
                    "2024_TOP100": "rgba(135,206,250,0.5)",
                    "2025_VIP": "rgba(255,165,0,1)",
                    "2025_TOP100": "blue"
                }
            )
            # 기준 월 강조
            ref_month_int = int(ref_month)  # 예: 기준 월 "2"
            fig.add_vrect(
                x0=ref_month_int - 0.5,
                x1=ref_month_int + 0.5,
                fillcolor="LightSalmon",
                opacity=0.3,
                layer="below",
                line_width=0
            )
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("TOP100 / VIP 관리몰 데이터를 불러올 수 없습니다.")

    ###################################
    # 탭 D[2]: 카테고리별 매출
    ###################################
    with tabs_D[2]:
        # [1] 섹션 제목
        st.subheader("EC전체 거래액 매출 추이")
        
        # 데이터 확인 (EC전체 카테고리 데이터)
        if 'df_ec_category' in st.session_state and st.session_state['df_ec_category'] is not None:
            df_ec = st.session_state['df_ec_category']
            
            # 카테고리 목록 (첫 번째 열 제외)
            categories = df_ec.columns[1:].tolist()
            date_column = df_ec.columns[0]  # 첫 번째 열(날짜/기간)
            
            # 데이터의 마지막 행(최신 데이터)
            latest_data = df_ec.iloc[-1]
            
            # 전년 동월 데이터 (13개월 전 데이터가 있다면)
            last_year_data = None
            if len(df_ec) > 12:
                last_year_data = df_ec.iloc[-13]  # 작년 같은 달
            
            # 전월 데이터
            prev_month_data = None
            if len(df_ec) > 1:
                prev_month_data = df_ec.iloc[-2]  # 전월
            
            # 카테고리별 YoY 계산
            category_yoy = {}
            category_amount_change = {}
            
            for cat in categories:
                if last_year_data is not None and pd.notna(last_year_data[cat]) and last_year_data[cat] != 0:
                    # 실제 데이터를 사용하여 YoY 계산
                    yoy = ((latest_data[cat] - last_year_data[cat]) / last_year_data[cat]) * 100
                    amount_change = latest_data[cat] - last_year_data[cat]
                    
                    # 데이터 저장
                    category_yoy[cat] = yoy
                    category_amount_change[cat] = amount_change
                else:
                    # 작년 데이터가 없거나 0인 경우, 0으로 설정
                    category_yoy[cat] = 0
                    category_amount_change[cat] = 0
            
            # df_sales에서 전체 거래액 데이터 가져오기
            total_yoy = 0
            total_jo = 0
            total_eok = 0
            
            if 'df_sales' in st.session_state and not st.session_state['df_sales'].empty:
                df_sales = st.session_state['df_sales']
                
                # 최신 데이터와 작년 동월 데이터 추출
                latest_sales = df_sales.iloc[-1]
                last_year_sales = None
                if len(df_sales) > 12:
                    last_year_sales = df_sales.iloc[-13]
                
                # 전체 거래액 증가율 계산
                if last_year_sales is not None and '전체' in latest_sales and '전체' in last_year_sales:
                    try:
                        current_total = float(latest_sales['전체'])
                        last_year_total = float(last_year_sales['전체'])
                        
                        if last_year_total > 0:
                            total_yoy = ((current_total - last_year_total) / last_year_total) * 100
                            total_amount_change = current_total - last_year_total
                            
                            # 총 증가액 조/억 단위로 변환 (원 → 억)
                            # df_sales에서는 이미 원단위로 저장되어 있다고 가정
                            total_amount_change_billion = total_amount_change / 100000000
                            total_jo = int(total_amount_change_billion // 10000)
                            total_eok = int(total_amount_change_billion % 10000)
                    except Exception as e:
                        st.error(f"전체 거래액 증가율 계산 중 오류: {e}")
            else:
                # df_sales 데이터가 없는 경우, 기존 로직으로 계산
                # 모든 카테고리의 합계를 이용하여 계산
                total_current = sum(latest_data[cat] for cat in categories if pd.notna(latest_data[cat]))
                total_last_year = 0
                if last_year_data is not None:
                    total_last_year = sum(last_year_data[cat] for cat in categories if pd.notna(last_year_data[cat]))
                
                # YoY 증가율 계산
                if total_last_year > 0:
                    total_yoy = ((total_current - total_last_year) / total_last_year) * 100
                    total_amount_change = total_current - total_last_year
                    # 총 증가액 조/억 단위로 변환 (원 → 억)
                    total_amount_change_billion = total_amount_change / 100000000
                    total_jo = int(total_amount_change_billion // 10000)
                    total_eok = int(total_amount_change_billion % 10000)
            
            # 최근 데이터의 날짜 정보 가져오기
            ref_date = "25년 2월"  # 기본값
            if 'df_sales' in st.session_state and not st.session_state['df_sales'].empty:
                try:
                    latest_sales = st.session_state['df_sales'].iloc[-1]
                    if '해당월' in latest_sales:
                        date_parts = latest_sales['해당월'].split('-')
                        if len(date_parts) == 2:
                            year = date_parts[0][2:]  # 4자리 연도에서 뒤 2자리만
                            month = date_parts[1]
                            ref_date = f"{year}년 {month}월"
                except Exception:
                    pass  # 기본값 유지
            
            # [2] 검정색 박스 - 전체 증가율 및 설명
            st.markdown(f"""
            <div style="
                background-color:#111; 
                border-radius:0px; 
                color:white; 
                padding:20px; 
                margin-bottom:20px; 
                display:flex;
            ">
            <!-- 왼쪽 큰 숫자 -->
            <div style="
                flex:1; 
                text-align:center; 
                font-size:24px; 
                font-weight:bold; 
                line-height:1.2;
            ">
                <span style="font-size:48px; display:block;">{total_yoy:.1f}%<span style="font-size:18px;">&#9650;</span></span>
                <span style="font-size:16px;">전년 동월 대비</span>
                <div style="font-size:14px; margin-top:10px;">+{total_jo}조 {total_eok:,}억</div>
            </div>

            <!-- 오른쪽 설명 문구 -->
            <div style="
                flex:3; 
                margin-left:20px; 
                font-size:16px; 
                line-height:1.5;
            ">
                <p style="margin:0;">
                <strong>{ref_date}</strong>은 전년 동월 대비 
                <strong style="color:#FFD700;">{total_yoy:.1f}%</strong> 상승하며, 
                전월 대비 YoY도 소폭 상승하였습니다. 전반적으로 모든 카테고리 매출이 상승하여 
                특히 <strong>식품</strong>, <strong>생활/건강</strong> 카테고리에서 매출을 견인한 반면, 
                <strong>패션의류</strong>는 하락하였습니다.
                </p>
            </div>
            </div>
            """, unsafe_allow_html=True)
            
            # [3] 카테고리별 YoY 정보 패널을 우측에 표시하고 차트를 메인 영역에 표시
            col_main, col_right = st.columns([3, 1])
            
            with col_right:
                # 카테고리별 YoY 정보 패널
                st.markdown("### 카테고리별 YoY")
                
                # 각 카테고리별로 패널 생성
                for cat, yoy in category_yoy.items():
                    # 금액을 억 단위로 변환 (원 단위 → 억 단위)
                    amount_in_billion = category_amount_change[cat] // 100000000
                    arrow_symbol = "▼" if yoy < 0 else "▲"
                    arrow_color = "blue" if yoy < 0 else "red"
                    
                    st.markdown(f"""
                        <div style="
                            border: 1px solid #e1e4e8; 
                            border-radius: 4px; 
                            padding: 10px; 
                            margin-bottom: 10px;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            background-color: white;
                        ">
                            <div style="font-weight: bold;">{cat}</div>
                            <div style="
                                font-weight: bold; 
                                color: {arrow_color}; 
                                font-size: 18px;
                            ">
                                {abs(yoy):.1f}% {arrow_symbol} <span style="font-size: 14px; color: #666;">+{amount_in_billion}억</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
            with col_main:
                # [4] 통합 차트 생성
                # 데이터 준비
                df_chart = df_ec.copy()
                
                # df_sales 데이터를 df_chart에 통합
                if 'df_sales' in st.session_state and not st.session_state['df_sales'].empty:
                    df_sales = st.session_state['df_sales'].copy()
                    
                    # 날짜 형식이 동일한지 확인 후 통합
                    try:
                        # df_sales의 '해당월' 컬럼과 df_chart의 첫 번째 컬럼(날짜) 비교
                        df_sales_dates = df_sales['해당월'].tolist()
                        df_chart_dates = df_chart[date_column].tolist()
                        
                        # 공통 날짜 찾기
                        common_dates = list(set(df_sales_dates) & set(df_chart_dates))
                        
                        # 'EC전체' 컬럼 추가
                        df_chart['EC전체'] = None
                        
                        # 공통 날짜에 대해 df_sales의 '전체' 값을 df_chart의 'EC전체'에 할당
                        for date in common_dates:
                            sales_value = df_sales.loc[df_sales['해당월'] == date, '전체'].values[0]
                            df_chart.loc[df_chart[date_column] == date, 'EC전체'] = float(sales_value)
                        
                    except Exception as e:
                        st.error(f"데이터 통합 중 오류: {e}")
                        # 오류 발생 시 기존 방식으로 'EC전체' 계산
                        df_chart['EC전체'] = df_chart[categories].sum(axis=1)
                else:
                    # df_sales 데이터가 없는 경우, 기존 방식으로 'EC전체' 계산
                    df_chart['EC전체'] = df_chart[categories].sum(axis=1)
                
                # 데이터를 억 단위로 변환
                df_chart_billions = df_chart.copy()
                for cat in ['EC전체'] + categories:
                    if cat in df_chart_billions.columns:
                        df_chart_billions[cat] = df_chart_billions[cat].astype(float) / 100000000  # 원 단위 → 억 단위로 변환

                # 통합 차트 생성 (억 단위 데이터 사용)
                fig = px.line(
                    df_chart_billions,
                    x=date_column,
                    y=['EC전체'] + categories,
                    title="EC전체 카테고리별 매출 추이",
                    labels={
                        date_column: "월",
                        "value": "거래액(억원)",
                        "variable": "카테고리"
                    }
                )
                
                # EC전체 라인은 두껍게, 나머지는 얇게 설정
                for i, trace in enumerate(fig.data):
                    if i == 0:  # EC전체 (첫 번째 트레이스)
                        trace.line.width = 3
                        trace.line.color = 'orange'
                
                # 레이아웃 설정
                fig.update_layout(
                    height=600,
                    xaxis_title="월",
                    yaxis_title="거래액(억원)",  # 단위 변경 반영
                    plot_bgcolor="white",
                    xaxis=dict(
                        tickmode='array',
                        tickvals=df_chart_billions[date_column].tolist(),
                        tickangle=45
                    ),
                    yaxis=dict(
                        tickformat=",",  # 쉼표로 구분된 숫자 형식
                        exponentformat="none"  # 지수 형식 사용 안 함
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),
                    margin=dict(l=50, r=50, t=80, b=100)
                )
                
                # 차트 표시
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.warning("EC전체 카테고리 데이터가 없습니다. 구글 시트 연결을 확인해주세요.")


        st.subheader("관리몰 거래액")
        st.write("관리몰 거래액 차트 추가예정")
        st.subheader("25년 N월 매출 증감 ")
        st.write("25년 N월 매출 증감 차트 추가예정")
        st.markdown(
            """
            <style>
            div[role="checkbox"] label {
                white-space: nowrap;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        try:
            # 구글 시트에서 "카테고리별" 시트 데이터 불러오기
            category_ws = client.open_by_key("1hrpu7fL5b7zQnwGwLTfq5tx3WtNJ-ZTeEiVWGhzbkx4").worksheet("카테고리별")
            category_data = category_ws.get_all_values()
            if len(category_data) > 1:
                header = category_data[0]
                rows = category_data[1:]
                df_category = pd.DataFrame(rows, columns=header)
            else:
                st.warning("카테고리별 시트에 데이터가 충분하지 않습니다.")
                df_category = pd.DataFrame()
        except Exception as e:
            st.error(f"카테고리별 시트 데이터를 불러오는 중 오류가 발생했습니다: {e}")
            df_category = pd.DataFrame()
        
        if not df_category.empty:
            # "카테고리" 컬럼명을 기준으로 고유값 추출 (컬럼명이 없으면 4번째 컬럼 사용)
            if "카테고리" in df_category.columns:
                unique_categories = df_category["카테고리"].dropna().unique().tolist()
            else:
                unique_categories = df_category.iloc[:, 3].dropna().unique().tolist()
            
            # 정렬 후 "기타" 항목은 맨 뒤로 배치
            unique_categories = sorted(unique_categories)
            if "기타" in unique_categories:
                unique_categories.remove("기타")
            unique_categories.append("기타")
        
            # 드롭다운 필터
            selected_category = st.selectbox("카테고리 선택", unique_categories)
            st.write("드롭다운 선택:", selected_category)
        
            # 체크박스 필터 (한 행에 7개씩)
            st.write("카테고리 선택 (체크박스)")
            selected_categories_check = []
            chunk_size = 7
            for i in range(0, len(unique_categories), chunk_size):
                row_cats = unique_categories[i : i + chunk_size]
                cols = st.columns(7)
                for col_idx in range(7):
                    if col_idx < len(row_cats):
                        cat = row_cats[col_idx]
                        if cols[col_idx].checkbox(cat, key=f"checkbox_{cat}"):
                            selected_categories_check.append(cat)
                    else:
                        cols[col_idx].write("")
        
            st.write("체크박스 선택:", selected_categories_check)
        else:
            st.info("카테고리별 데이터가 없습니다.")

    ###################################
    # 탭 D[3]: 카페24 EC 전체
    ###################################
    with tabs_D[3]:
        st.subheader("카페24 EC 전체")
        if 'df_sales' in st.session_state and not st.session_state['df_sales'].empty:
            df_sales = st.session_state['df_sales']
            latest_data = df_sales.iloc[-1]
            prev_month_data = df_sales.iloc[-2] if len(df_sales) > 1 else None
            last_year_same_month = df_sales.iloc[-13] if len(df_sales) > 12 else None
            ref_date = latest_data['해당월']
            ref_year, ref_month = ref_date.split("-")
            ref_date_str = f"{ref_year}년 {ref_month}월 기준"
            st.markdown(f"**데이터 기준: {ref_date_str}**")



            col1, col2, col3 = st.columns(3)
            with col1:
                total_revenue = float(latest_data['전체'])
                prev_month_change = total_revenue - float(prev_month_data['전체']) if prev_month_data is not None else 0
                prev_month_percent = (prev_month_change / float(prev_month_data['전체']) * 100) if prev_month_data is not None and float(prev_month_data['전체']) != 0 else 0
                last_year_change = 0
                last_year_percent = 0
                if last_year_same_month is not None:
                    last_year_total = float(last_year_same_month['전체'])
                    last_year_change = total_revenue - last_year_total
                    last_year_percent = (last_year_change / last_year_total * 100) if last_year_total != 0 else 0

                prev_month_arrow = "▲" if prev_month_change >= 0 else "▼"
                last_year_arrow = "▲" if last_year_change >= 0 else "▼"

                total_revenue_display = format_currency(int(total_revenue / 100000000))
                prev_month_change_display = format_currency(int(abs(prev_month_change) / 100000000))
                last_year_change_display = format_currency(int(abs(last_year_change) / 100000000))

                st.markdown(f"""
                <div class="modern-card">
                    <h4>EC 전체 매출</h4>
                    <div class="value">{total_revenue_display}</div>
                    <div class="badge green">{prev_month_arrow} 전월 대비 {prev_month_percent:.1f}%({prev_month_change_display})</div>
                    <div class="badge blue">{last_year_arrow} 전년 대비 {last_year_percent:.1f}%({last_year_change_display})</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                badge_color = "red" if prev_month_percent < 0 else "blue"
                st.markdown(f"""
                <div class="modern-card">
                    <h4>전월 매출 대비</h4>
                    <div class="value">{prev_month_percent:.1f}%</div>
                    <div class="badge {badge_color}">{prev_month_arrow} {prev_month_change_display}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                badge_color = "green" if last_year_percent > 0 else "red"
                st.markdown(f"""
                <div class="modern-card">
                    <h4>작년 동일월 대비</h4>
                    <div class="value">{last_year_percent:.1f}%</div>
                    <div class="badge {badge_color}">{last_year_arrow} {last_year_change_display}</div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("월별 매출 원본 데이터"):
                df_display = df_sales[['해당월', '전체']].copy()
                df_display['전체'] = df_display['전체'].apply(lambda x: format_currency(int(x/100000000)) if pd.notnull(x) else "")
                st.dataframe(df_display)
            with st.expander("📊 월간 분석(샘플)", expanded=True):
                st.markdown("""
                - EC 전체 매출 전년 대비 7.8% 상승
                - 신규 입점 몰 증가 (전월 대비 15개 증가)
                - 주요 업종: 화장품, 건강식품 매출 강세
                - 해외 판매 비중 확대 (전체 매출의 12.5%)
                """)
            if df_sales is not None:
                df_chart_ec = df_sales.copy()
                df_chart_ec['전체'] = df_chart_ec['전체'] / 100_000_000
                df_chart_ec['해당월_dt'] = pd.to_datetime(df_chart_ec['해당월'], errors='coerce')
                df_chart_ec = df_chart_ec.dropna(subset=['해당월_dt'])
                df_chart_ec['Year'] = df_chart_ec['해당월_dt'].dt.year
                df_chart_ec['Month'] = df_chart_ec['해당월_dt'].dt.month

                current_year = datetime.date.today().year
                target_years = [current_year - 2, current_year - 1, current_year]
                df_filtered_ec = df_chart_ec[df_chart_ec['Year'].isin(target_years)]

                fig_ec = px.line(
                    df_filtered_ec,
                    x='Month',
                    y='전체',
                    color='Year',
                    markers=True,
                    labels={'Month': '월', '전체': '매출(억 원)'},
                    title="카페24 EC 전체 월별 매출 현황 (연도별 비교)"
                )

                ref_month_int = int(ref_month)
                fig_ec.add_vrect(
                    x0=ref_month_int - 0.5,
                    x1=ref_month_int + 0.5,
                    fillcolor="LightSalmon",
                    opacity=0.3,
                    layer="below",
                    line_width=0
                )

                fig_ec.update_xaxes(dtick=1)
                fig_ec.update_yaxes(
                    tickformat=".0f",
                    ticksuffix="억"
                )
                st.plotly_chart(fig_ec, use_container_width=True)
        else:
            st.warning("카페24 EC 전체 데이터를 불러올 수 없습니다.")

    ###################################
    # 탭 D[4]: 디지털트윈
    ###################################
    with tabs_D[4]:
        # 제목 및 레이아웃 설정
        st.markdown("<h2 style='margin-bottom: 20px;'>고객 관계</h2>", unsafe_allow_html=True)
        
        # 메인 지표와 상세 지표 영역 생성
        col_main, col_detailed = st.columns([1, 3])
        
        with col_main:
            # 메인 지표 스타일 정의
            st.markdown("""
            <style>
            .main-metrics-card {
                background-color: #000000;
                border-radius: 10px;
                padding: 15px;
                color: white;
            }
            .period-header {
                text-align: center;
                padding: 10px 0;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            .metric-row {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #333;
            }
            .metric-row:last-child {
                border-bottom: none;
            }
            .metric-name {
                font-size: 16px;
            }
            .metric-value {
                text-align: right;
            }
            .metric-change {
                display: inline-block;
                margin-left: 10px;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            .positive {
                background-color: #b8c7dc;
                color: black;
            }
            .neutral {
                background-color: #999999;
                color: black;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # 메인 지표 내용 (별도로 렌더링)
            st.markdown("""
            <div class="main-metrics-card">
                <div class="period-header">25년 3월 3주차</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 각 지표를 개별적으로 렌더링하여 에러 가능성 감소
            st.markdown("""
            <div class="main-metrics-card" style="margin-top: -16px; border-top-left-radius: 0; border-top-right-radius: 0;">
                <div class="metric-row">
                    <div class="metric-name">대면/비대면</div>
                    <div class="metric-value">
                        00건/00건
                        <span class="metric-change positive">99% ▲</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="main-metrics-card" style="margin-top: -16px; border-radius: 0;">
                <div class="metric-row">
                    <div class="metric-name">서비스 연결</div>
                    <div class="metric-value">
                        00건
                        <span class="metric-change neutral">0% ▲</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="main-metrics-card" style="margin-top: -16px; border-radius: 0;">
                <div class="metric-row">
                    <div class="metric-name">비즈 플랜</div>
                    <div class="metric-value">
                        00건
                        <span class="metric-change neutral">0% ▲</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="main-metrics-card" style="margin-top: -16px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;">
                <div class="metric-row">
                    <div class="metric-name">주요 키워드</div>
                    <div class="metric-value">
                        00건
                        <span class="metric-change positive">+48% ▲</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_detailed:
            st.markdown("<h3>상세 지표</h3>", unsafe_allow_html=True)
            
            # 첫 번째 행의 차트들
            cols = st.columns(3)
            
            # 대면/비대면 도넛 차트
            with cols[0]:
                st.markdown("<div style='border: 1px solid #e6e6e6; border-radius: 10px; padding: 15px;'>", unsafe_allow_html=True)
                st.markdown("<div style='display: flex; justify-content: space-between; margin-bottom: 15px;'><span style='font-weight: bold;'>대면/비대면</span><span>📊</span></div>", unsafe_allow_html=True)
                
                # Streamlit에 내장된 함수를 사용하여 도넛 차트 생성
                fig1_data = {
                    'Category': ['대면/비대면', '기타'],
                    'Value': [99, 1]  # 99%와 1%
                }
                fig1_df = pd.DataFrame(fig1_data)
                fig1 = px.pie(fig1_df, values='Value', names='Category', hole=0.7, 
                            color_discrete_sequence=['#a9a9a9', '#f0f0f0'])
                fig1.update_layout(
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0),
                    annotations=[dict(text="00건/00건", x=0.5, y=0.5, font_size=14, showarrow=False)]
                )
                st.plotly_chart(fig1, use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 서비스 연결 도넛 차트
            with cols[1]:
                st.markdown("<div style='border: 1px solid #e6e6e6; border-radius: 10px; padding: 15px;'>", unsafe_allow_html=True)
                st.markdown("<div style='display: flex; justify-content: space-between; margin-bottom: 15px;'><span style='font-weight: bold;'>서비스 연결</span><span>📊</span></div>", unsafe_allow_html=True)
                
                fig2_data = {
                    'Category': ['서비스 연결', '기타'],
                    'Value': [21, 79]  # 21%와 79%
                }
                fig2_df = pd.DataFrame(fig2_data)
                fig2 = px.pie(fig2_df, values='Value', names='Category', hole=0.7, 
                            color_discrete_sequence=['#a9a9a9', '#f0f0f0'])
                fig2.update_layout(
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0),
                    annotations=[dict(text="21%", x=0.5, y=0.5, font_size=16, showarrow=False)]
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 비즈 플랜 도넛 차트
            with cols[2]:
                st.markdown("<div style='border: 1px solid #e6e6e6; border-radius: 10px; padding: 15px;'>", unsafe_allow_html=True)
                st.markdown("<div style='display: flex; justify-content: space-between; margin-bottom: 15px;'><span style='font-weight: bold;'>비즈 플랜</span><span>📊</span></div>", unsafe_allow_html=True)
                
                fig3_data = {
                    'Category': ['비즈 플랜', '기타'],
                    'Value': [43, 57]  # 43%와 57%
                }
                fig3_df = pd.DataFrame(fig3_data)
                fig3 = px.pie(fig3_df, values='Value', names='Category', hole=0.7, 
                            color_discrete_sequence=['#a9a9a9', '#f0f0f0'])
                fig3.update_layout(
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0),
                    annotations=[dict(text="43%", x=0.5, y=0.5, font_size=16, showarrow=False)]
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 두 번째 행 - 주요 키워드 도넛 차트
            st.markdown("<div style='border: 1px solid #e6e6e6; border-radius: 10px; padding: 15px; margin-top: 20px;'>", unsafe_allow_html=True)
            st.markdown("<div style='display: flex; justify-content: space-between; margin-bottom: 15px;'><span style='font-weight: bold;'>주요 키워드</span><span>📊</span></div>", unsafe_allow_html=True)
            
            fig4_data = {
                'Category': ['주요 키워드', '기타'],
                'Value': [99, 1]  # 99%와 1%
            }
            fig4_df = pd.DataFrame(fig4_data)
            fig4 = px.pie(fig4_df, values='Value', names='Category', hole=0.7, 
                        color_discrete_sequence=['#a9a9a9', '#f0f0f0'])
            fig4.update_layout(
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0),
                height=250,
                annotations=[dict(text="99%", x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            st.plotly_chart(fig4, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------
# (C) 사이드바 정보 (try: 밖)
# ---------------------------------------
st.sidebar.markdown("---")
st.sidebar.info("각 Topic별로 탭/차트, 또는 구글 시트 데이터를 확인할 수 있습니다.")