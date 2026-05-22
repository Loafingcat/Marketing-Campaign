import streamlit as st
import pandas as pd

from utils.data_loader import load_csv_data
from utils.preprocessing import preprocess_data
from utils.filters import apply_sidebar_filters
from utils.metrics import calculate_metrics

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Overview")

df = load_csv_data()
df = preprocess_data(df)

if df.empty:
    st.warning("데이터가 없습니다. data 폴더에 CSV 파일을 넣거나 Data Upload 페이지를 사용하세요.")
    st.stop()

filtered_df = apply_sidebar_filters(df)

st.subheader("핵심 성과 지표")

metrics = calculate_metrics(filtered_df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Campaigns", f"{metrics['total_campaigns']:,}")

with col2:
    st.metric("Impressions", f"{metrics['total_impressions']:,.0f}")

with col3:
    st.metric("Clicks", f"{metrics['total_clicks']:,.0f}")

with col4:
    st.metric("Conversions", f"{metrics['total_conversions']:,.0f}")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Total Spend", f"${metrics['total_spend']:,.0f}")

with col6:
    st.metric("Total Revenue", f"${metrics['total_revenue']:,.0f}")

with col7:
    st.metric("CTR", f"{metrics['ctr'] * 100:.2f}%")

with col8:
    st.metric("ROAS / ROI", f"{metrics['avg_roi']:.2f}")

st.divider()

st.subheader("필터 적용 데이터")
st.dataframe(filtered_df, use_container_width=True)

st.download_button(
    label="필터링된 데이터 CSV 다운로드",
    data=filtered_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="filtered_marketing_campaign.csv",
    mime="text/csv"
)