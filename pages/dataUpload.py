import streamlit as st
import pandas as pd

from utils.data_loader import load_uploaded_data
from utils.preprocessing import preprocess_data

st.set_page_config(
    page_title="Data Upload",
    page_icon="📁",
    layout="wide"
)

st.title("📁 Data Upload & Campaign Simulator")

st.markdown("""
이 페이지에서는 CSV 파일을 직접 업로드해서 데이터를 확인할 수 있습니다.  
또한 간단한 캠페인 예상 성과 계산 form을 제공합니다.
""")

uploaded_file = st.file_uploader(
    "CSV 파일 업로드",
    type=["csv"]
)

if uploaded_file is not None:
    uploaded_df = load_uploaded_data(uploaded_file)
    uploaded_df = preprocess_data(uploaded_df)

    st.success("CSV 파일 업로드 완료")

    st.subheader("업로드 데이터 미리보기")
    st.dataframe(uploaded_df.head(30), use_container_width=True)

    st.subheader("기본 통계")
    st.dataframe(uploaded_df.describe(include="all"), use_container_width=True)

    st.download_button(
        label="전처리된 CSV 다운로드",
        data=uploaded_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="preprocessed_campaign_data.csv",
        mime="text/csv"
    )

st.divider()

st.subheader("캠페인 예상 성과 계산기")

with st.form("campaign_simulator_form"):
    budget = st.number_input(
        "예산",
        min_value=0.0,
        value=1000.0,
        step=100.0
    )

    expected_cpc = st.number_input(
        "예상 CPC",
        min_value=0.01,
        value=1.5,
        step=0.1
    )

    expected_conversion_rate = st.slider(
        "예상 전환율",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
        step=0.01
    )

    average_order_value = st.number_input(
        "평균 주문 금액",
        min_value=0.0,
        value=50.0,
        step=5.0
    )

    submitted = st.form_submit_button("예상 성과 계산")

if submitted:
    expected_clicks = budget / expected_cpc if expected_cpc > 0 else 0
    expected_conversions = expected_clicks * expected_conversion_rate
    expected_revenue = expected_conversions * average_order_value
    expected_roas = expected_revenue / budget if budget > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("예상 클릭 수", f"{expected_clicks:,.0f}")

    with col2:
        st.metric("예상 전환 수", f"{expected_conversions:,.0f}")

    with col3:
        st.metric("예상 매출", f"${expected_revenue:,.0f}")

    with col4:
        st.metric("예상 ROAS", f"{expected_roas:.2f}")