import pandas as pd


def safe_sum(df: pd.DataFrame, col: str) -> float:
    if col in df.columns:
        return float(df[col].sum())
    return 0.0


def safe_mean(df: pd.DataFrame, col: str) -> float:
    if col in df.columns:
        return float(df[col].mean())
    return 0.0


def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    대시보드 상단 metric 카드에 사용할 값 계산
    """
    total_campaigns = len(df)

    total_impressions = safe_sum(df, "Impressions")
    total_clicks = safe_sum(df, "Clicks")
    total_conversions = safe_sum(df, "Conversions")
    total_spend = safe_sum(df, "Spend")
    total_revenue = safe_sum(df, "Revenue")

    ctr = total_clicks / total_impressions if total_impressions > 0 else 0
    conversion_rate = total_conversions / total_clicks if total_clicks > 0 else 0
    roas = total_revenue / total_spend if total_spend > 0 else 0

    if "ROI" in df.columns:
        avg_roi = safe_mean(df, "ROI")
    elif "ROAS" in df.columns:
        avg_roi = safe_mean(df, "ROAS")
    else:
        avg_roi = roas

    return {
        "total_campaigns": total_campaigns,
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "total_spend": total_spend,
        "total_revenue": total_revenue,
        "ctr": ctr,
        "conversion_rate": conversion_rate,
        "roas": roas,
        "avg_roi": avg_roi
    }