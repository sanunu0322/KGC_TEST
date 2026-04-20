import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64
from datetime import datetime

# 1. 페이지 설정 (가장 상단에 위치해야 함)
st.set_page_config(page_title="KGC 브랜드 전략실 - 주간 마케팅 통찰", layout="wide")

# 2. PDF 클래스 정의 (한글 지원을 고려한 구조)
class KGC_PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'KGC Weekly Marketing Report', 0, 1, 'C')
        self.ln(5)

def generate_pdf():
    pdf = KGC_PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    content = [
        "Product: Everyday Balance (Renewal)",
        f"Report Date: {datetime.now().strftime('%Y-%m-%d')}",
        "-------------------------------------------",
        "1. Sales Performance",
        "- Metropolitan: +15% (Convenience Store Strength)",
        "- Local: -2% (Mart Stagnation)",
        "",
        "2. Customer Insights",
        "- Main Buyer: 2030 Social Newcomers (45%)",
        "- Outdoor Trend: Hiking/Tennis mentions increased 30%",
        "",
        "3. Strategy",
        "- Strengthen Outdoor TPO Marketing",
        "- Optimize Convenience Store Promotions"
    ]
    
    for line in content:
        pdf.cell(0, 10, txt=line, ln=True)
    
    # latin-1 대신 latin-1 에러 방지를 위해 핸들링
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- UI 시작 ---
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
    st.metric("아웃도어 키워드", "+30%", delta="HOT")

st.divider()

# 4. 시각화 섹션
left_column, right_column = st.columns(2)
with left_column:
    st.markdown("### 📍 지역별 판매 추이")
    region_data = pd.DataFrame({'지역': ['수도권', '지방'], '증감률': [15, -2]})
    fig_region = px.bar(region_data, x='지역', y='증감률', color='지역', 
                         color_discrete_sequence=['#D32F2F', '#757575'])
    st.plotly_chart(fig_region, use_container_width=True)

with right_column:
    st.markdown("### 🎯 주요 구매층 분석")
    age_data = pd.DataFrame({'연령층': ['2030', '기타'], '비중': [45, 55]})
    fig_age = px.pie(age_data, values='비중', names='연령층', hole=.4,
                      color_discrete_sequence=['#D32F2F', '#E0E0E0'])
    st.plotly_chart(fig_age, use_container_width=True)

# 5. 고객 인사이트
st.divider()
st.markdown("### 💬 고객 보이스(VOC) 및 마케팅 통찰")
con1, con2 = st.columns(2)
with con1:
    st.success("**긍정 피드백**\n- 패키지 세련미 호평\n- 쓴맛 완화로 음용 편의성 증대")
    st.error("**부정 피드백**\n- 가격 인상 체감도 높음\n- 개봉 시 뻑뻑함 개선 필요")
with con2:
    st.info("**💡 팀장 전략 제언**\n- 아웃도어 트렌드 결합 마케팅 강화\n- 2030 타겟 편의점 소포장 프로모션 확대")

# 6. 사이드바 - PDF 리포트 생성 (중복 제거됨)
st.sidebar.title("📄 Report Management")
st.sidebar.write("분석 데이터를 PDF로 추출합니다.")

if st.sidebar.button("PDF 리포트 생성"):
    try:
        pdf_bytes = generate_pdf()
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="KGC_Weekly_Report.pdf" style="text-decoration: none;"><button style="width: 100%; padding: 10px; background-color: #D32F2F; color: white; border: none; border-radius: 5px; cursor: pointer;">📥 PDF 다운로드 받기</button></a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
        st.sidebar.success("리포트 생성이 완료되었습니다.")
    except Exception as e:
        st.sidebar.error(f"PDF 생성 중 오류 발생: {e}")
