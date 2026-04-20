import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="KGC 브랜드 전략실 - 마케팅 대시보드", layout="wide")

# 2. 데이터 정의
REPORT_DATE = "2026년 3월 4주차"
PRODUCT_NAME = "정관장 에브리타임 밸런스 (리뉴얼)"

# 3. PDF 생성 함수
def create_pdf(data_summary):
    pdf = FPDF()
    pdf.add_page()
    
    # 폰트 설정 (기본 폰트는 한글 깨짐이 발생하므로, 배포 시 한글 폰트 파일 포함 권장)
    # 여기서는 구조적 설계를 위해 영문/숫자 중심 레이아웃 예시를 보여드립니다.
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Weekly Marketing Insight Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {REPORT_DATE}", ln=True)
    pdf.cell(200, 10, txt=f"Product: {PRODUCT_NAME}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Key Metrics", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"- Metropolitan Sales: +15%", ln=True)
    pdf.cell(200, 10, txt=f"- Local Sales: -2%", ln=True)
    pdf.cell(200, 10, txt=f"- Target (2030s): 45%", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Strategic Insights", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="1. Strong performance in convenience stores within metropolitan areas.\n"
                             "2. Outdoor keywords (Hiking, Tennis) increased by 30%.\n"
                             "3. Need to address price sensitivity and packaging convenience.")
    
    return pdf.output(dest='S').encode('latin-1')

# 4. 메인 대시보드 UI
st.title("🚀 브랜드 전략실 주간 대시보드")
st.subheader(f"{PRODUCT_NAME} | {REPORT_DATE}")

# 상단 KPI 메트릭
col1, col2, col3, col4 = st.columns(4)
col1.metric("수도권 판매", "+15%", help="편의점 채널 강세")
col2.metric("지방 판매", "-2%", delta="-2%", delta_color="inverse")
col3.metric("2030 구매층", "45%", "핵심 타겟")
col4.metric("아웃도어 키워드", "+30%", delta="HOT")

st.divider()

# 차트 섹션
left, right = st.columns(2)
with left:
    st.markdown("### 📍 지역별 성장률")
    df_reg = pd.DataFrame({'Region': ['Metropolitan', 'Local'], 'Growth': [15, -2]})
    fig_reg = px.bar(df_reg, x='Region', y='Growth', color='Region', 
                     color_discrete_sequence=['#D32F2F', '#757575'])
    st.plotly_chart(fig_reg, use_container_width=True)

with right:
    st.markdown("### 🎯 타겟 연령층 비중")
    df_age = pd.DataFrame({'Group': ['2030s', 'Others'], 'Value': [45, 55]})
    fig_age = px.pie(df_age, values='Value', names='Group', hole=0.4,
                     color_discrete_sequence=['#D32F2F', '#E0E0E0'])
    st.plotly_chart(fig_age, use_container_width=True)

# 인사이트 요약
st.divider()
st.markdown("### 💬 마케팅 인사이트 & VOC")
c1, c2 = st.columns(2)
with c1:
    st.info("✅ **Strength & Opportunity**\n- 리뉴얼 패키지 디자인 호평\n- 테니스/등산 등 MZ 세대 아웃도어 트렌드와 결합")
with c2:
    st.warning("⚠️ **Weakness & Threat**\n- 가격 저항감 존재\n- 패키지 개봉 편의성(빡빡함) 개선 건의")

# 5. PDF 다운로드 기능 (사이드바)
st.sidebar.header("📊 Report Export")
st.sidebar.write("현재 데이터를 기반으로 PDF 리포트를 생성합니다.")

if st.sidebar.button("Generate PDF Report"):
    try:
        pdf_data = create_pdf(None)
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="KGC_Report_{datetime.now().strftime("%Y%m%d")}.pdf" style="text-decoration: none;"><button style="width: 100%; cursor: pointer; background-color: #D32F2F; color: white; border: none; padding: 10px; border-radius: 5px;">📥 Download PDF Report</button></a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
        st.sidebar.success("리포트 준비 완료!")
    except Exception as e:
        st.sidebar.error(f"오류 발생: {e}")

st.sidebar.divider()
st.sidebar.caption("KGC Brand Strategy Team v1.0")
