import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from base64 import b64encode

# [중요] PDF 출력을 위해 추가된 함수
def generate_pdf_download_link():
    # 실제 운영 환경에서는 아래 생성된 PDF 파일을 읽어와서 다운로드 링크로 변환합니다.
    with open("KGC_Weekly_Insight_Report.pdf", "rb") as f:
        pdf_base64 = b64encode(f.read()).decode()
    
    return f'<a href="data:application/pdf;base64,{pdf_base64}" download="KGC_Report_2026_03_4W.pdf">📥 클릭하여 PDF 보고서 다운로드</a>'

# 1. 페이지 설정
st.set_page_config(page_title="KGC 브랜드 전략실 - 주간 마케팅 통찰", layout="wide")

# 2. 데이터 정의 (주어진 데이터 반영)
st.title("🚀 정관장 에브리타임 밸런스 마케팅 대시보드")
st.subheader("2026년 3월 4주차 분석 보고")

# 3. KPI 메트릭 섹션
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("수도권 판매량", "+15%", delta_color="normal")
with col2:
    st.metric("지방 판매량", "-2%", delta="-2%")
with col3:
    st.metric("2030 구매 비중", "45%")
with col4:
    st.metric("아웃도어 키워드 언급", "+30%", delta="HOT")

st.divider()

# 4. 시각화 섹션
left_column, right_column = st.columns(2)

with left_column:
    st.markdown("### 📍 지역별 판매 추이")
    region_data = pd.DataFrame({
        '지역': ['수도권', '지방'],
        '증감률': [15, -2]
    })
    fig_region = px.bar(region_data, x='지역', y='증감률', 
                         color='지역', color_discrete_sequence=['#D32F2F', '#757575'])
    st.plotly_chart(fig_region, use_container_width=True)

with right_column:
    st.markdown("### 🎯 주요 구매층 분석 (Age Group)")
    age_data = pd.DataFrame({
        '연령층': ['2030 사회초년생', '기타'],
        '비중': [45, 55]
    })
    fig_age = px.pie(age_data, values='비중', names='연령층', hole=.4,
                      color_discrete_sequence=['#D32F2F', '#E0E0E0'])
    st.plotly_chart(fig_age, use_container_width=True)

# 5. 고객 인사이트 (Sentiment Analysis)
st.divider()
st.markdown("### 💬 고객 보이스(VOC) 및 마케팅 통찰")
con1, con2 = st.columns(2)

with con1:
    st.success("**긍정 피드백 (Strength)**\n- 리뉴얼 패키지 세련미 호평\n- 맛의 대중화 성공 (쓴맛 완화)")
    st.error("**부정 피드백 (Weakness)**\n- 가격 인상 체감도 높음\n- 패키징 개봉 편의성 개선 필요")

with con2:
    st.info("**💡 팀장 전략 제언**\n- **TPO 확장:** 등산/테니스 키워드 급증에 따른 스포츠 마케팅 강화\n- **채널 최적화:** 편의점 채널 강세를 이용한 1+1 또는 소포장 프로모션 제안")

# 6. PDF 리포트 추출 섹션 (사이드바 또는 하단)
st.sidebar.divider()
st.sidebar.markdown("### 📄 보고서 관리")
if st.sidebar.button("PDF 리포트 생성"):
    st.sidebar.success("리포트가 생성되었습니다!")
    st.sidebar.markdown(generate_pdf_download_link(), unsafe_allow_html=True)
