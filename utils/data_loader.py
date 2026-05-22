import os
import pandas as pd
import streamlit as st

DEFAULT_DATA_PATH = "data/marketing_campaign_dataset.xls"


@st.cache_data
def load_csv_data(file_path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """
    기본 CSV 파일을 불러오는 함수
    - data 폴더 안에 CSV 파일이 있으면 자동 로드
    - 없으면 빈 DataFrame 반환
    """
    if not os.path.exists(file_path):
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    return df


@st.cache_data
def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    """
    사용자가 업로드한 CSV 파일을 불러오는 함수
    """
    if uploaded_file is None:
        return pd.DataFrame()

    df = pd.read_csv(uploaded_file)
    return df