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
st.write("### 📅 請選擇要處理或查閱的班務項目：")

if st.button("📝 01_每日聯絡簿與歷史紀錄查詢系統", use_container_width=True):
    st.session_state["page_contact_auth"] = True
    
    possible_pages = [
        "pages/每日聯絡簿.py",
        "pages/01_每日聯絡簿.py",
        "pages/01_聯絡簿管理.py",
        "pages/每日聯絡簿管理.py",
        "01_聯絡簿管理.py",
        "每日聯絡簿.py"
    ]
    
    switched = False
    for p in possible_pages:
        try:
            st.switch_page(p)
            switched = True
            break
        except Exception:
            continue
            
    if not switched:
        st.error("⚠️ 找不到聯絡簿頁面檔案，請確認 pages/ 資料夾內的 Python 檔名。")
