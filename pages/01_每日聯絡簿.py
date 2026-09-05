import os
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="01_每日聯絡簿與作業催收", page_icon="📝", layout="wide")

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
    .item-label { color: #1E40AF !important; font-size: 15px !important; font-weight: 800 !important; margin-top: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# 教師驗證機制
if "page_contact_auth" not in st.session_state:
    st.session_state["page_contact_auth"] = False

if not st.session_state["page_contact_auth"]:
    st.write("### 🔒 教師安全驗證專區")
    with st.form("page_auth_form"):
        p = st.text_input("請輸入 5 位數導師密碼：", type="password")
        if st.form_submit_button("確認通行"):
            if p.strip() == "12345":
                st.session_state["page_contact_auth"] = True
                st.rerun()
            else:
                st.error("❌ 密碼錯誤。")
    if st.button("⬅️ 返回管理主控台", use_container_width=True):
        try: st.switch_page("main.py")
        except: st.switch_page("app.py")
    st.stop()

# 標頭與返回按鈕
col_top_title, col_top_back = st.columns([0.80, 0.20])
with col_top_title:
    st.write("# 📝 801 每日聯絡簿、作業與催收管理系統")
with col_top_back: 
    if st.button("🏛️ 返回管理主控台", use_container_width=True):
        try: st.switch_page("main.py")
        except: st.switch_page("app.py")

# 檔案路徑設定
FILE_NAME = "801班_導師班務紀錄總表.xlsx"
TXT_ITEM_FILE = "長期催收清單.txt"
TXT_STATUS_FILE = "長期催收狀態紀錄.txt"
TXT_HW_ITEM_FILE = "每日作業清單.txt"
TXT_HW_STATUS_FILE = "每日作業狀態紀錄.txt"

student_names = [
    "王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", 
    "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", 
    "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", 
    "董子以", "劉家佑", "魏辰恩"
]
seat_list = [int(i+1) for i in range(len(student_names))]

# 讀寫通用工具函式
def load_list_from_file(filepath):
    if not os.path.exists(filepath): return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def load_status_from_file(filepath, items):
    status_dict = {item: {seat: "未繳 ❌" for seat in seat_list} for item in items}
    if not os.path.exists(filepath): return status_dict
    try:
        with open(filepath, "r", encoding="utf-8") as f:
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

def save_status_to_file(filepath, status_dict):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for item, seats in status_dict.items():
                for seat, status in seats.items(): 
                    f.write(f"{item},{seat},{status}\n")
    except: pass

# 回調函數（即時寫入狀態與觸發廣播台更新）
def update_item_status_callback(category, item_name, seat_num, key_name):
    new_val = st.session_state[key_name]
    if category == "lt":
        st.session_state["long_term_status"][item_name][seat_num] = new_val
        save_status_to_file(TXT_STATUS_FILE, st.session_state["long_term_status"])
    elif category == "hw":
        st.session_state["hw_status"][item_name][seat_num] = new_val
        save_status_to_file(TXT_HW_STATUS_FILE, st.session_state["hw_status"])

def load_daily_data(target_date):
    df_def = pd.DataFrame({"座號": seat_list, "姓名": student_names, "聯絡簿簽名": "已簽 📝", "生活札記": "已寫 🗒️", "備註事項": ""})
    if not os.path.exists(FILE_NAME):
        try:
            with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w: 
                df_def.to_excel(w, sheet_name=target_date, index=False)
        except: pass
        return df_def
    try:
        with pd.ExcelFile(FILE_NAME, engine="openpyxl") as xl:
            if target_date in xl.sheet_names: 
                df = pd.read_excel(xl, sheet_name=target_date)
                df["備註事項"] = df["備註事項"].fillna("")
                return df
            else: 
                return df_def.copy()
    except: 
        return df_def.copy()

def save_daily_data(updated_df, target_date):
    try:
        sheets_data = {}
        if os.path.exists(FILE_NAME):
            try:
                with pd.ExcelFile(FILE_NAME, engine="openpyxl") as xl:
                    for sheet in xl.sheet_names:
                        if sheet != target_date: 
                            sheets_data[sheet] = pd.read_excel(xl, sheet_name=sheet)
            except: sheets_data = {}
        sheets_data[target_date] = updated_df
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
            for sheet, s_df in sheets_data.items(): 
                s_df.to_excel(w, sheet_name=sheet, index=False)
    except: pass

def get_all_history_dates():
    if not os.path.exists(FILE_NAME): return []
    try:
        with pd.ExcelFile(FILE_NAME, engine="openpyxl") as xl:
            return sorted(xl.sheet_names, reverse=True)
    except: return []

# 初始化記憶體狀態
long_term_items = load_list_from_file(TXT_ITEM_FILE)
hw_items = load_list_from_file(TXT_HW_ITEM_FILE)

if "long_term_status" not in st.session_state:
    st.session_state["long_term_status"] = load_status_from_file(TXT_STATUS_FILE, long_term_items)

if "hw_status" not in st.session_state:
    st.session_state["hw_status"] = load_status_from_file(TXT_HW_STATUS_FILE, hw_items)

tab_daily, tab_history = st.tabs(["📝 每日登記與催收廣播", "🔍 歷史總覽與個人查詢"])

with tab_daily:
    col_left_panel, col_right_students = st.columns([0.28, 0.72])

    with col_left_panel:
        st.write("### 📅 選擇登記項目")
        current_date = st.date_input("選擇聯絡簿登記/補登日期：", datetime.now(), key="main_date")
        date_str = current_date.strftime("%Y-%m-%d")
        df_daily = load_daily_data(date_str)
        
        # 下拉選單整合：聯絡簿、作業、長期催收
        menu_options = ["📝 每日聯絡簿與札記"] + [f"📚 作業：{i}" for i in hw_items] + [f"📋 催收：{i}" for i in long_term_items]
        current_view = st.selectbox("🎯 請選擇右側要登記的項目：", menu_options, key="view_selector")

        st.markdown("---")
        st.write("### ➕ 新增追蹤項目")
        col_a, col_b = st.columns(2)
        with col_a:
            new_hw = st.text_input("新增日常作業：", placeholder="如: 數學習作", key="input_hw")
            if st.button("確認新增作業", use_container_width=True):
                if new_hw and new_hw not in hw_items:
                    with open(TXT_HW_ITEM_FILE, "a", encoding="utf-8") as f: f.write(f"{new_hw}\n")
                    st.session_state["hw_status"][new_hw] = {seat: "未繳 ❌" for seat in seat_list}
                    save_status_to_file(TXT_HW_STATUS_FILE, st.session_state["hw_status"])
                    st.rerun()
        with col_b:
            new_item = st.text_input("新增長期催收：", placeholder="如: HPV同意書", key="input_lt")
            if st.button("確認新增催收", use_container_width=True):
                if new_item and new_item not in long_term_items:
                    with open(TXT_ITEM_FILE, "a", encoding="utf-8") as f: f.write(f"{new_item}\n")
                    st.session_state["long_term_status"][new_item] = {seat: "未繳 ❌" for seat in seat_list}
                    save_status_to_file(TXT_STATUS_FILE, st.session_state["long_term_status"])
                    st.rerun()

        st.markdown("---")
        st.write("### 📢 即時催繳廣播台")
        
        # 廣播台核心邏輯
        if current_view == "📝 每日聯絡簿與札記":
            df_ns = df_daily[df_daily["聯絡簿簽名"] == "未簽 ❌"]
            if not df_ns.empty:
                t_s = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
                st.text_area("📋 複製傳至家長群組：", value=t_s, height=110, key="c_s")
            else: st.success("🎉 本日聯絡簿全班皆已簽名！")

            df_nd = df_daily[df_daily["生活札記"] == "未寫 ❌"]
            if not df_nd.empty:
                t_d = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
                st.text_area("📋 複製傳至班級群組：", value=t_d, height=110, key="c_d")
            else: st.success("🎉 本日生活札記全班皆已完成！")
            
        elif current_view.startswith("📚 作業："):
            selected_hw_name = current_view.replace("📚 作業：", "")
            item_status_map = st.session_state["hw_status"].get(selected_hw_name, {})
            unpaid_students = [seat for seat, status in item_status_map.items() if status == "未繳 ❌"]
            
            if unpaid_students:
                t_i = f"【801班 {selected_hw_name} 尚未繳交名單】\n"
                for seat in unpaid_students:
                    name = student_names[seat_list.index(seat)]
                    t_i += f"{seat}號 {name}\n"
                st.text_area(f"📋 複製 {selected_hw_name} 催繳文字：", value=t_i, height=180, key=f"c_bc_hw_{selected_hw_name}")
            else: 
                st.success(f"💯 {selected_hw_name} 全班皆已繳齊！")

        elif current_view.startswith("📋 催收："):
            selected_lt_name = current_view.replace("📋 催收：", "")
            item_status_map = st.session_state["long_term_status"].get(selected_lt_name, {})
            unpaid_students = [seat for seat, status in item_status_map.items() if status == "未繳 ❌"]
            
            if unpaid_students:
                t_i = f"【801班 {selected_lt_name} 尚未繳交名單】\n"
                for seat in unpaid_students:
                    name = student_names[seat_list.index(seat)]
                    t_i += f"{seat}號 {name}\n"
                st.text_area(f"📋 複製 {selected_lt_name} 催繳文字：", value=t_i, height=180, key=f"c_bc_lt_{selected_lt_name}")
            else: 
                st.success(f"💯 {selected_lt_name} 全班皆已繳齊！")

    with col_right_students:
        if current_view == "📝 每日聯絡簿與札記": 
            st.write(f"### 📅 紀錄登記區：{date_str} 聯絡簿與札記")
        elif current_view.startswith("📚 作業："):
            st.write(f"### 📚 作業繳交登記：{current_view.replace('📚 作業：', '')}")
        else:
            st.write(f"### 📋 長期催收登記：{current_view.replace('📋 催收：', '')}")
        st.write("")

        for i in range(0, len(student_names), 4):
            grid = st.columns(4)
            for idx_grid in range(4):
                student_idx = i + idx_grid
                if student_idx < len(student_names):
                    seat_num = seat_list[student_idx]
                    name_s = student_names[student_idx]
                    gender_icon = "🌸" if seat_num <= 14 else "🍀"
                    
                    with grid[idx_grid].container(border=True):
                        st.markdown(f'### <span style="white-space:nowrap;">{gender_icon} {seat_num}號 {name_s}</span>', unsafe_allow_html=True)
                        st.write("")
                        
                        if current_view == "📝 每日聯絡簿與札記":
                            row_s = df_daily[df_daily["座號"] == seat_num].iloc[0]
                            ns = st.radio(f"聯絡簿_{seat_num}", ["已簽 📝", "未簽 ❌"], index=(0 if row_s["聯絡簿簽名"] == "已簽 📝" else 1), horizontal=True, key=f"s_{seat_num}_{date_str}")
                            nd = st.radio(f"札記_{seat_num}", ["已寫 🗒️", "未寫 ❌"], index=(0 if row_s["生活札記"] == "已寫 🗒️" else 1), horizontal=True, key=f"d_{seat_num}_{date_str}")
                            if ns != row_s["聯絡簿簽名"] or nd != row_s["生活札記"]:
                                df_daily.loc[df_daily["座號"] == seat_num, "聯絡簿簽名"], df_daily.loc[df_daily["座號"] == seat_num, "生活札記"] = ns, nd
                                save_daily_data(df_daily, date_str)
                                st.rerun()
                            current_memo = "" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])
                            nm = st.text_input(f"備註_{seat_num}", value=current_memo, placeholder="隨手備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}")
                            if nm != current_memo:
                                df_daily.loc[df_daily["座號"] == seat_num, "備註事項"] = nm
                                save_daily_data(df_daily, date_str)
                        
                        elif current_view.startswith("📚 作業："):
                            hw_name = current_view.replace("📚 作業：", "")
                            if hw_name not in st.session_state["hw_status"]:
                                st.session_state["hw_status"][hw_name] = {seat: "未繳 ❌" for seat in seat_list}
                            
                            curr_st = st.session_state["hw_status"][hw_name].get(seat_num, "未繳 ❌")
                            r_key = f"r_hw_{hw_name}_{seat_num}"
                            
                            st.radio(
                                f"hw_{hw_name}_{seat_num}", ["已繳 ✅", "未繳 ❌"],
                                index=(0 if curr_st == "已繳 ✅" else 1), horizontal=True,
                                key=r_key, label_visibility="collapsed",
                                on_change=update_item_status_callback,
                                args=("hw", hw_name, seat_num, r_key)
                            )
                            
                        elif current_view.startswith("📋 催收："):
                            lt_name = current_view.replace("📋 催收：", "")
                            if lt_name not in st.session_state["long_term_status"]:
                                st.session_state["long_term_status"][lt_name] = {seat: "未繳 ❌" for seat in seat_list}
                            
                            curr_st = st.session_state["long_term_status"][lt_name].get(seat_num, "未繳 ❌")
                            r_key = f"r_lt_{lt_name}_{seat_num}"
                            
                            st.radio(
                                f"lt_{lt_name}_{seat_num}", ["已繳 ✅", "未繳 ❌"],
                                index=(0 if curr_st == "已繳 ✅" else 1), horizontal=True,
                                key=r_key, label_visibility="collapsed",
                                on_change=update_item_status_callback,
                                args=("lt", lt_name, seat_num, r_key)
                            )

    st.markdown("---")
    if current_view == "📝 每日聯絡簿與札記":
        st.markdown(f"### 📊 801班 {date_str} 聯絡簿總表")
        st.dataframe(df_daily, use_container_width=True)

with tab_history:
    st.write("### 📜 歷史班務紀錄查詢庫")
    all_dates = get_all_history_dates()
    
    if not all_dates:
        st.info("💡 目前尚無任何歷史紀錄，請先在「每日登記」分頁登記資料。")
    else:
        col_h1, col_h2 = st.columns([0.5, 0.5])
        
        with col_h1:
            selected_h_date = st.selectbox("📅 選擇要查看歷史紀錄的日期：", all_dates)
            if selected_h_date:
                df_h = load_daily_data(selected_h_date)
                st.write(f"#### 📊 {selected_h_date} 當日紀錄總表")
                st.dataframe(df_h, use_container_width=True)
                
        with col_h2:
            st.write("#### 👤 特定學生歷史紀錄追蹤")
            search_student = st.selectbox("選擇學生姓名：", student_names)
            
            if search_student:
                student_seat = seat_list[student_names.index(search_student)]
                st.write(f"##### 🔎 【{student_seat}號 {search_student}】歷史全紀錄：")
                
                records = []
                for d in all_dates:
                    df_tmp = load_daily_data(d)
                    row_tmp = df_tmp[df_tmp["座號"] == student_seat]
                    if not row_tmp.empty:
                        r = row_tmp.iloc[0]
                        records.append({
                            "日期": d,
                            "聯絡簿簽名": r["聯絡簿簽名"],
                            "生活札記": r["生活札記"],
                            "備註事項": r["備註事項"]
                        })
                
                df_person = pd.DataFrame(records)
                st.dataframe(df_person, use_container_width=True)

        st.markdown("---")
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "rb") as f:
                st.download_button(
                    label="📥 下載完整 801 班務 Excel 歷史總表",
                    data=f,
                    file_name=FILE_NAME,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
