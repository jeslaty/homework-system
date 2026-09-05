import os
import streamlit as st

st.set_page_config(page_title="801班務管理主控台", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea { 
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", sans-serif !important; 
    }
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="stSidebarContent"], 
    button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"], #MainMenu, header[data-testid="stHeader"] { 
        display: none !important; 
        visibility: hidden !important; 
        width: 0px !important; 
        height: 0px !important; 
    }
    </style>
""", unsafe_allow_html=True)

st.write("# 🏛️ 801 班級事務管理主控台")
st.write("---")
st.write("### 📅 請選擇今日要處理的獨立班務項目：")

# 嘗試自動偵測子頁面檔名與位置
target_page = "pages/01_聯絡簿管理.py"
if not os.path.exists(target_page):
    target_page = "01_聯絡簿管理.py"

if st.button("📝 01_聯絡簿管理系統", use_container_width=True):
    # 傳送已驗證狀態給目標頁面
    st.query_params["auth"] = "passed"
    st.switch_page(target_page)
