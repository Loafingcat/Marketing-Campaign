import streamlit as st
import plotly.express as px

from utils.data_loader import load_csv_data
from utils.preprocessing import preprocess_data
from utils.filters import apply_sidebar_filters

st.set_page_config(
    page_title="Campaign Charts",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Campaign Charts")

df = load_csv_data()
df = preprocess_data(df)

if df.empty:
    st.warning("데이터가 없습니다. data 폴더에 CSV 파일을 넣거나 Data Upload 페이지를 사용하세요.")
    st.stop()

filtered_df = apply_sidebar_filters(df)

st.subheader("차트 시각화")

category_options = [
    col for col in [
        "Campaign_Type",
        "Campaign_Name",
        "Channel",
        "Marketing_Channel",
        "Target_Audience",
        "Customer_Segment",
        "Location",
        "Language"
    ]
    if col in filtered_df.columns
]

numeric_options = [
    col for col in [
        "Impressions",
        "Clicks",
        "Conversions",
        "Spend",
        "Revenue",
        "ROI",
        "ROAS",
        "CTR",
        "Conversion_Rate_Calc",
        "CPC",
        "CPA"
    ]
    if col in filtered_df.columns
]

if not category_options or not numeric_options:
    st.error("시각화에 필요한 범주형 컬럼 또는 숫자형 컬럼이 부족합니다.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    selected_category = st.selectbox(
        "분석 기준 컬럼",
        category_options
    )

with col2:
    selected_metric = st.selectbox(
        "성과 지표 컬럼",
        numeric_options
    )

chart_df = (
    filtered_df
    .groupby(selected_category, as_index=False)[selected_metric]
    .sum()
    .sort_values(selected_metric, ascending=False)
)

col3, col4 = st.columns(2)

with col3:
    st.markdown("### Bar Chart")
    fig_bar = px.bar(
        chart_df,
        x=selected_category,
        y=selected_metric,
        title=f"{selected_category}별 {selected_metric}",
        text_auto=True
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.markdown("### Pie Chart")
    fig_pie = px.pie(
        chart_df,
        names=selected_category,
        values=selected_metric,
        title=f"{selected_category}별 {selected_metric} 비중"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

if "Spend" in filtered_df.columns and "Revenue" in filtered_df.columns:
    st.markdown("### Spend vs Revenue")

    scatter_color = selected_category if selected_category in filtered_df.columns else None

    fig_scatter = px.scatter(
        filtered_df,
        x="Spend",
        y="Revenue",
        color=scatter_color,
        size="Conversions" if "Conversions" in filtered_df.columns else None,
        hover_data=filtered_df.columns,
        title="광고비 대비 매출 분포"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

if "Impressions" in filtered_df.columns and "Clicks" in filtered_df.columns:
    st.markdown("### Impressions vs Clicks")

    fig_click = px.scatter(
        filtered_df,
        x="Impressions",
        y="Clicks",
        color=selected_category,
        title="노출 수 대비 클릭 수"
    )
    st.plotly_chart(fig_click, use_container_width=True)