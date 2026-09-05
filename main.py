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

# 頁面路徑設定 (請依據你的實際檔案名稱調整)
p1 = "pages/01_聯絡簿管理.py" 

# 若你的子頁面就在 pages 資料夾下，可以使用安全的 query_params 帶入驗證狀態
if os.path.exists(p1):
    st.page_link(
        p1, 
        label="📝 01_聯絡簿管理系統", 
        use_container_width=True, 
        query_params={"auth": "passed"}
    )
else:
    # 備用路徑 (若檔案未放在 pages 資料夾內)
    st.page_link(
        "01_聯絡簿管理.py", 
        label="📝 01_聯絡簿管理系統", 
        use_container_width=True, 
        query_params={"auth": "passed"}
    )
