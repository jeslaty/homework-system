import streamlit as st

st.set_page_config(page_title="801 班務管理主控台", page_icon="🏫", layout="wide")

st.write("# 🏫 801 導師班務管理系統")
st.write("請選擇要進行管理的項目：")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("📝 每日聯絡簿與長期催收")
        st.write("包含：聯絡簿簽名、生活札記登記、HPV同意書等獨立催收項目與廣播台。")
        if st.button("前往聯絡簿專區 ➔", use_container_width=True):
            st.switch_page("pages/01_每日聯絡簿.py") # 請確認這裡的檔名與 pages/ 內的檔名一致

with col2:
    with st.container(border=True):
        st.subheader("📚 每日作業登記")
        st.write("包含：各科作業登記、欠繳學生廣播文字產生。")
        if st.button("前往作業登記專區 ➔", use_container_width=True):
            st.switch_page("pages/02_作業登記.py") # 請確認這裡的檔名與 pages/ 內的檔名一致
