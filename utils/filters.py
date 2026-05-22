import pandas as pd
import streamlit as st


def get_existing_columns(df: pd.DataFrame, candidates: list[str]) -> list[str]:
    """
    후보 컬럼 중 실제 데이터에 존재하는 컬럼만 반환
    """
    return [col for col in candidates if col in df.columns]


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    사이드바 필터 적용
    데이터셋 컬럼명이 조금 달라도 동작하도록 후보 컬럼 기반으로 구성
    """
    filtered_df = df.copy()

    st.sidebar.header("필터 설정")

    category_candidates = [
        "Campaign_Type",
        "Campaign_Name",
        "Channel",
        "Marketing_Channel",
        "Target_Audience",
        "Customer_Segment",
        "Location",
        "Language"
    ]

    category_columns = get_existing_columns(filtered_df, category_candidates)

    for col in category_columns:
        unique_values = sorted(filtered_df[col].dropna().unique().tolist())

        selected_values = st.sidebar.multiselect(
            label=f"{col} 선택",
            options=unique_values,
            default=unique_values
        )

        if selected_values:
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

    numeric_candidates = [
        "Impressions",
        "Clicks",
        "Conversions",
        "Spend",
        "Revenue",
        "ROI",
        "ROAS",
        "CTR",
        "Conversion_Rate_Calc"
    ]

    numeric_columns = get_existing_columns(filtered_df, numeric_candidates)

    with st.sidebar.expander("숫자 범위 필터"):
        for col in numeric_columns:
            min_value = float(filtered_df[col].min())
            max_value = float(filtered_df[col].max())

            if min_value == max_value:
                continue

            selected_range = st.slider(
                label=f"{col} 범위",
                min_value=min_value,
                max_value=max_value,
                value=(min_value, max_value)
            )

            filtered_df = filtered_df[
                (filtered_df[col] >= selected_range[0]) &
                (filtered_df[col] <= selected_range[1])
            ]

    return filtered_df