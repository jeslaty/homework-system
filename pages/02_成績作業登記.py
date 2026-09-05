import os
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="02_每日作業登記專區", page_icon="📚", layout="wide")

# 精準 CSS 樣式，隱藏側邊欄
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
    </style>
""", unsafe_allow_html=True)

# 驗證機制
if "page_hw_auth" not in st.session_state:
    st.session_state["page_hw_auth"] = False

if not st.session_state["page_hw_auth"]:
    st.write("### 🔒 教師安全驗證專區")
    with st.form("hw_auth_form"):
        p = st.text_input("請輸入 5 位數導師密碼：")
        if st.form_submit_button("確認通行"):
            if p.strip() == "12345":
                st.session_state["page_hw_auth"] = True
                st.rerun()
            else:
                st.error("❌ 密碼錯誤。")
    if st.button("⬅️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")
    st.stop()

col_top_title, col_top_back = st.columns([0.80, 0.20])
with col_top_title:
    st.write("# 📚 801 每日各科作業與成績登記系統")
with col_top_back: 
    if st.button("🏛️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")

FILE_HW_ITEMS = "作業催收清單.txt"
FILE_HW_STATUS = "作業催收狀態紀錄.txt"

# 完整 27 人名單
student_names = [
    "王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", 
    "黃榆涵", "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", 
    "王駿展", "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", 
    "黃楙軒", "董子以", "劉家佑", "魏辰恩"
]
seat_list = [int(i+1) for i in range(len(student_names))]

def load_hw_items():
    if not os.path.exists(FILE_HW_ITEMS): return ["國文作業", "數學講義"]
    with open(FILE_HW_ITEMS, "r", encoding="utf-8") as f: 
        items = [line.strip() for line in f.readlines() if line.strip()]
        return items if items else ["國文作業", "數學講義"]

def load_hw_status(items):
    status_dict = {item: {seat: "未繳 ❌" for seat in seat_list} for item in items}
    if not os.path.exists(FILE_HW_STATUS): return status_dict
    try:
        with open(FILE_HW_STATUS, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "," in line:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        item, seat_str_num, status = parts
                        seat_num = int(seat_str_num)
                        if item in status_dict and seat_num in status_dict[item]: 
                            status_dict[item][seat_num] = status
    except: pass
    return status_dict

def save_hw_status():
    if "hw_status" in st.session_state:
        try:
            with open(FILE_HW_STATUS, "w", encoding="utf-8") as f:
                for item, seats in st.session_state["hw_status"].items():
                    for seat, status in seats.items(): 
                        f.write(f"{item},{seat},{status}\n")
        except: pass

def on_hw_change(item_name, seat_num, widget_key):
    new_val = st.session_state[widget_key]
    st.session_state["hw_status"][item_name][seat_num] = new_val
    save_hw_status()

hw_items = load_hw_items()

if "hw_status" not in st.session_state:
    st.session_state["hw_status"] = load_hw_status(hw_items)

col_left_panel, col_right_students = st.columns([0.28, 0.72])

with col_left_panel:
    st.write("### 📌 作業與測驗項目選擇")
    current_hw_view = st.selectbox("🎯 請選擇右側要登記的作業：", hw_items, key="hw_selector")

    st.markdown("---")
    new_hw_item = st.text_input("➕ 新增作業/測驗項目：", placeholder="例如：國文L1小考、英文習作", key="new_hw_input")
    if st.button("確認建立作業項目", use_container_width=True):
        if new_hw_item and new_hw_item not in hw_items:
            try:
                with open(FILE_HW_ITEMS, "a", encoding="utf-8") as f: f.write(f"{new_hw_item}\n")
                st.session_state["hw_status"][new_hw_item] = {seat: "未繳 ❌" for seat in seat_list}
                save_hw_status()
                st.rerun()
            except: st.error("⚠️ 寫入失敗，請重試。")

    st.markdown("---")
    st.write("### 📢 作業缺交廣播台")
    
    item_status_map = st.session_state["hw_status"].get(current_hw_view, {})
    unpaid_students = [seat for seat, status in item_status_map.items() if status == "未繳 ❌"]
    
    if unpaid_students:
        t_i = f"【801班 {current_hw_view} 缺交名單】\n"
        for seat in unpaid_students:
            name = student_names[seat_list.index(seat)]
            t_i += f"{seat}號 {name}\n"
        st.text_area(
            f"📋 複製 {current_hw_view} 催繳文字：", 
            value=t_i, 
            height=220, 
            key=f"hw_broadcast_{current_hw_view}_{len(unpaid_students)}_{sum(unpaid_students)}"
        )
    else: 
        st.success(f"💯 {current_hw_view} 全班皆已繳齊！")

with col_right_students:
    st.write(f"### 📋 作業與成績登記區：{current_hw_view}")
    st.write("")

    for i in range(0, len(student_names), 4):
        grid = st.columns(4)
        for idx_grid in range(4):
            student_idx = i + idx_grid
            if student_idx < len(student_names):
                seat_num = seat_list[student_idx]
                name_s = student_names[student_idx]
                gender_icon = "🌸" if seat_num <= 15 else "🍀"
                
                with grid[idx_grid].container(border=True):
                    st.markdown(f'### <span style="white-space:nowrap;">{gender_icon} {seat_num}號 {name_s}</span>', unsafe_allow_html=True)
                    st.write("")
                    
                    if current_hw_view not in st.session_state["hw_status"]:
                        st.session_state["hw_status"][current_hw_view] = {seat: "未繳 ❌" for seat in seat_list}
                    
                    current_status = st.session_state["hw_status"][current_hw_view].get(seat_num, "未繳 ❌")
                    r_key = f"r_hw_{current_hw_view}_{seat_num}"
                    
                    st.radio(
                        f"{current_hw_view}_{seat_num}", 
                        ["已繳 ✅", "未繳 ❌"], 
                        index=(0 if current_status == "已繳 ✅" else 1), 
                        horizontal=True, 
                        key=r_key, 
                        label_visibility="collapsed",
                        on_change=on_hw_change,
                        args=(current_hw_view, seat_num, r_key)
                    )
                    if st.session_state.get(r_key) and st.session_state[r_key] != current_status:
                        st.rerun()
