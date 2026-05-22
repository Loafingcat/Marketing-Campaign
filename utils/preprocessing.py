import pandas as pd
import numpy as np


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    컬럼명을 코드에서 쓰기 쉽게 정리
    예:
    Campaign Name -> Campaign_Name
    Acquisition Cost -> Acquisition_Cost
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("/", "_")
    )
    return df


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    숫자로 변환 가능한 컬럼을 숫자형으로 변환
    $, %, 콤마 등이 섞여 있어도 처리
    """
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == "object":
            cleaned = (
                df[col]
                .astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
                .str.strip()
            )

            converted = pd.to_numeric(cleaned, errors="coerce")

            if converted.notna().sum() > 0 and converted.notna().sum() >= len(df) * 0.5:
                df[col] = converted

    return df


def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    날짜형으로 보이는 컬럼을 datetime으로 변환
    """
    df = df.copy()

    date_keywords = ["date", "start", "end"]

    for col in df.columns:
        lower_col = col.lower()

        if any(keyword in lower_col for keyword in date_keywords):
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    결측치 처리
    - 숫자형: 중앙값
    - 문자형: Unknown
    """
    df = df.copy()

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")

    return df


def add_calculated_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    분석에 필요한 파생 컬럼 생성
    가능한 컬럼이 있을 때만 계산
    """
    df = df.copy()

    if "Clicks" in df.columns and "Impressions" in df.columns:
        df["CTR"] = np.where(
            df["Impressions"] > 0,
            df["Clicks"] / df["Impressions"],
            0
        )

    if "Conversions" in df.columns and "Clicks" in df.columns:
        df["Conversion_Rate_Calc"] = np.where(
            df["Clicks"] > 0,
            df["Conversions"] / df["Clicks"],
            0
        )

    if "Spend" in df.columns and "Clicks" in df.columns:
        df["CPC"] = np.where(
            df["Clicks"] > 0,
            df["Spend"] / df["Clicks"],
            0
        )

    if "Spend" in df.columns and "Conversions" in df.columns:
        df["CPA"] = np.where(
            df["Conversions"] > 0,
            df["Spend"] / df["Conversions"],
            0
        )

    if "Revenue" in df.columns and "Spend" in df.columns:
        df["ROAS"] = np.where(
            df["Spend"] > 0,
            df["Revenue"] / df["Spend"],
            0
        )

    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    전체 전처리 파이프라인
    """
    if df.empty:
        return df

    df = clean_column_names(df)
    df = convert_numeric_columns(df)
    df = convert_date_columns(df)
    df = handle_missing_values(df)
    df = add_calculated_columns(df)

    return df