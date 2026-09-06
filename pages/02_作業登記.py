import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="02_作業登記專區", page_icon="📚", layout="wide")

# CSS 隱藏側邊欄
st.markdown("""
    <style>
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

# 頂部導覽
col_top_title, col_top_back = st.columns([0.80, 0.20])
with col_top_title:
    st.write("# 📚 全校各科作業登記系統")
with col_top_back: 
    if st.button("🏛️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")

# --- 四個班級名單（含真實座號與姓名） ---
CLASSES_DATA = {
    "801班": [
        (1, '王喬昕'), (2, '吳岢曈'), (3, '李巧彤'), (4, '岳昀軒'), (5, '林晏以'), 
        (6, '林晨琳'), (7, '林芮妘'), (8, '林苡嫻'), (9, '黃榆涵'), (10, '黃榆涵'), 
        (11, '蔡可琳'), (12, '戴彤竹'), (13, '羅羽翎'), (14, '羅昕彤'), (15, '林禹彤'), 
        (16, '王楷文'), (17, '王駿展'), (18, '吳軒佑'), (19, '李宇哲'), (20, '林柏辰'), 
        (21, '張品御'), (22, '陳正澤'), (23, '陳秉玄'), (24, '陳鼎硯'), (25, '黃楙軒'), 
        (26, '董子以'), (27, '劉家佑'), (28, '魏辰恩')
    ],
    "903班": [
        (1, '張莘妍'), (2, '梁芯瑜'), (3, '吳佳錹'), (4, '許秧秧'), (5, '陳又綺'), 
        (6, '高筱媗'), (7, '莊子玉'), (8, '吳愷昕'), (9, '陳以恩'), (10, '蕭妤柔'), 
        (11, '吳璥齡'), (12, '魏品儀'), (15, '邱子恆'), (16, '張本維'), (17, '謝易宸'), 
        (18, '游子宥'), (19, '吳宇曜'), (20, '吳嘉恩'), (21, '丁沛紳'), (22, '林子佑'), 
        (23, '陳冠成'), (24, '徐國睿'), (25, '余冠憲'), (26, '黃家寶'), (27, '張瑋志'), 
        (28, '方仲祺'), (29, '林昱嘉')
    ],
    "904班": [
        (1, '戴嘉妤'), (2, '陳資晴'), (3, '傅詩穎'), (4, '張瞳恩'), (5, '黃宇婕'), 
        (6, '吳沛媛'), (7, '李妍芯'), (8, '鄭羽恩'), (9, '林子桐'), (10, '許詠晴'), 
        (11, '吳宸彤'), (12, '林品妍'), (15, '趙右群'), (16, '林定毅'), (17, '潘子堯'), 
        (18, '郭羿楷'), (19, '張明哲'), (20, '吳宇曜'), (21, '魏永聖'), (22, '游承恩'), 
        (23, '胡琮浩'), (24, '李柏沅'), (25, '許育政'), (26, '宗旻恩'), (27, '吳博硯')
    ],
    "906班": [
        (1, '陳亮妤'), (3, '董宜洳'), (4, '林庭瑜'), (5, '許淯淳'), (6, '陳鈺軒'), 
        (7, '林郁庭'), (8, '陳雅竹'), (9, '陳睿瑤'), (10, '楊淇暄'), (11, '陳雨萱'), 
        (12, '江霈穎'), (15, '陳逸恩'), (16, '劉哲皓'), (17, '陳士愷'), (18, '李開哲'), 
        (19, '林翊凱'), (20, '林晉宇'), (21, '林釉荏'), (22, '林均昊'), (23, '賴羿軒'), 
        (24, '鄧仲喆'), (25, '吳羽翔'), (26, '林擎宇'), (27, '林旻勳'), (28, '鄭凱軒'), 
        (29, '李秉叡'), (31, '曾群文'), (32, '吳立丞')
    ]
}

# --- 檔案處理函式 ---
def get_hw_files(class_name):
    item_file = f"{class_name}_作業催收清單.txt"
    status_file = f"{class_name}_作業催收狀態紀錄.txt"
    return item_file, status_file

def load_hw_items(class_name):
    item_file, _ = get_hw_files(class_name)
    if not os.path.exists(item_file): return ["國文作業", "數學講義"]
    with open(item_file, "r", encoding="utf-8") as f: 
        items = [line.strip() for line in f.readlines() if line.strip()]
        return items if items else ["國文作業", "數學講義"]

def load_hw_status(class_name, items, student_list):
    status_dict = {item: {seat: "未繳 ❌" for seat, _ in student_list} for item in items}
    _, status_file = get_hw_files(class_name)
    if not os.path.exists(status_file): return status_dict
    try:
        with open(status_file, "r", encoding="utf-8") as f:
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

def save_hw_status(class_name):
    key = f"hw_status_{class_name}"
    _, status_file = get_hw_files(class_name)
    if key in st.session_state:
        try:
            with open(status_file, "w", encoding="utf-8") as f:
                for item, seats in st.session_state[key].items():
                    for seat, status in seats.items(): 
                        f.write(f"{item},{seat},{status}\n")
        except: pass

def on_hw_change(class_name, item_name, seat_num, widget_key):
    new_val = st.session_state[widget_key]
    st.session_state[f"hw_status_{class_name}"][item_name][seat_num] = new_val
    save_hw_status(class_name)

# --- 主介面配置 ---
col_left_panel, col_right_students = st.columns([0.28, 0.72])

with col_left_panel:
    st.write("### 🏫 班級與項目選擇")
    
    # 1. 切換班級
    selected_class = st.selectbox("選擇班級：", list(CLASSES_DATA.keys()), key="class_selector")
    
    # 取得當前班級資料
    student_info = CLASSES_DATA[selected_class]
    seat_to_name = {seat: name for seat, name in student_info}
    hw_items = load_hw_items(selected_class)
    
    status_key = f"hw_status_{selected_class}"
    if status_key not in st.session_state:
        st.session_state[status_key] = load_hw_status(selected_class, hw_items, student_info)

    # 2. 選擇作業項目
    current_hw_view = st.selectbox("🎯 請選擇右側要登記的作業：", hw_items, key=f"hw_selector_{selected_class}")

    st.markdown("---")
    new_hw_item = st.text_input(f"➕ 為【{selected_class}】新增作業/測驗：", placeholder="例如：國文L1小考", key=f"new_hw_{selected_class}")
    if st.button("確認建立作業項目", use_container_width=True):
        if new_hw_item and new_hw_item not in hw_items:
            try:
                item_file, _ = get_hw_files(selected_class)
                with open(item_file, "a", encoding="utf-8") as f: f.write(f"{new_hw_item}\n")
                st.session_state[status_key][new_hw_item] = {seat: "未繳 ❌" for seat, _ in student_info}
                save_hw_status(selected_class)
                st.rerun()
            except: st.error("⚠️ 寫入失敗，請重試。")

    st.markdown("---")
    st.write("### 📢 作業缺交廣播台")
    
    item_status_map = st.session_state[status_key].get(current_hw_view, {})
    unpaid_students = [seat for seat, status in item_status_map.items() if status == "未繳 ❌"]
    
    if unpaid_students:
        t_i = f"【{selected_class} {current_hw_view} 缺交名單】\n"
        for seat in sorted(unpaid_students):
            name = seat_to_name.get(seat, "")
            t_i += f"{seat}號 {name}\n"
        st.text_area(
            f"📋 複製 {selected_class} 催繳文字：", 
            value=t_i, 
            height=200, 
            key=f"hw_bc_{selected_class}_{current_hw_view}_{len(unpaid_students)}_{sum(unpaid_students)}"
        )
    else: 
        st.success(f"💯 【{selected_class}】{current_hw_view} 全班皆已繳齊！")

with col_right_students:
    st.write(f"### 📋 【{selected_class}】作業登記區：{current_hw_view}")
    st.write("")

    for i in range(0, len(student_info), 4):
        grid = st.columns(4)
        for idx_grid in range(4):
            student_idx = i + idx_grid
            if student_idx < len(student_info):
                seat_num, name_s = student_info[student_idx]
                gender_icon = "🌸" if seat_num <= 15 else "🍀"
                
                with grid[idx_grid].container(border=True):
                    st.markdown(f'### <span style="white-space:nowrap;">{gender_icon} {seat_num}號 {name_s}</span>', unsafe_allow_html=True)
                    st.write("")
                    
                    if current_hw_view not in st.session_state[status_key]:
                        st.session_state[status_key][current_hw_view] = {seat: "未繳 ❌" for seat, _ in student_info}
                    
                    current_status = st.session_state[status_key][current_hw_view].get(seat_num, "未繳 ❌")
                    r_key = f"r_hw_{selected_class}_{current_hw_view}_{seat_num}"
                    
                    st.radio(
                        f"{current_hw_view}_{seat_num}", 
                        ["已繳 ✅", "未繳 ❌"], 
                        index=(0 if current_status == "已繳 ✅" else 1), 
                        horizontal=True, 
                        key=r_key, 
                        label_visibility="collapsed",
                        on_change=on_hw_change,
                        args=(selected_class, current_hw_view, seat_num, r_key)
                    )
                    if st.session_state.get(r_key) and st.session_state[r_key] != current_status:
                        st.rerun()
