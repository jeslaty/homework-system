import streamlit as st

st.set_page_config(
    page_title="導師與各科班務管理主控台", 
    page_icon="🏫", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    html, body, [class*="st-"], .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", sans-serif !important;
    }
    [data-testid="stSidebar"], 
    button[data-testid="collapsedControl"], 
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #64748B; margin-bottom: 2rem; }
    .card-box {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px;
        padding: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transition: all 0.3s ease;
    }
    .card-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
    .card-title { font-size: 1.35rem; font-weight: 700; color: #0F172A; margin-bottom: 0.5rem; }
    .card-desc { font-size: 0.95rem; color: #475569; line-height: 1.6; min-height: 3.2rem; margin-bottom: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏫 班務與教學管理主控台</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">整合導師班務日常、長期催收與全校各科作業登記系統</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
        <div class="card-box">
            <div class="card-icon">📝</div>
            <div class="card-title">801 導師班務與聯絡簿專區</div>
            <div class="card-desc">
                專屬 801 導師管理功能。<br>
                涵蓋：每日聯絡簿簽名、生活札記、隨手備註，以及行政同意書等長期催收廣播。
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🚀 前往導師班務專區", key="btn_contact", use_container_width=True, type="primary"):
        # 關鍵修正：不加 pages/ 前綴
        st.switch_page("01_每日聯絡簿.py")

with col2:
    st.markdown("""
        <div class="card-box">
            <div class="card-icon">📚</div>
            <div class="card-title">跨班作業與成績登記專區</div>
            <div class="card-desc">
                適用於任教班級作業管理。<br>
                支援：<b>801、903、904、906 班</b> 各科作業催收，即時產生家長群組廣播文字。
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🚀 前往作業登記專區", key="btn_hw", use_container_width=True, type="primary"):
        # 關鍵修正：檔名需與第一步重新命名的檔名完全一致
        st.switch_page("02_作業登記.py")

st.markdown("---")
st.info("💡 系統各分頁皆已設有安全密碼驗證（預設為 5 位數導師密碼：12345）。資料變更時會自動儲存，並支援即時一鍵複製廣播文字。")
