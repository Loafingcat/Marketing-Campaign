import streamlit as st
from utils.data_loader import load_csv_data
from utils.preprocessing import preprocess_data

st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Marketing Campaign Performance Dashboard")

st.markdown("""
이 대시보드는 Kaggle의 Marketing Campaign Performance Dataset을 기반으로  
마케팅 캠페인의 노출, 클릭, 전환, 비용, 수익, ROI 흐름을 분석하는 Streamlit 프로젝트입니다.
""")

df = load_csv_data()
df = preprocess_data(df)

if df.empty:
    st.warning("""
    아직 데이터가 로드되지 않았습니다.

    아래 경로에 CSV 파일을 넣어주세요.

    `data/marketing_campaign_dataset.csv`

    또는 왼쪽 페이지 메뉴에서 `Data Upload` 페이지를 사용하세요.
    """)
else:
    st.success("데이터 로드 완료")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("전체 행 수", f"{len(df):,}")

    with col2:
        st.metric("전체 컬럼 수", f"{len(df.columns):,}")

    with col3:
        duplicated_count = df.duplicated().sum()
        st.metric("중복 행 수", f"{duplicated_count:,}")

    st.subheader("데이터 미리보기")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("컬럼 정보")
    st.write(df.dtypes.astype(str))