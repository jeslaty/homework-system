import os
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="01_每日聯絡簿與歷史查詢", page_icon="📝", layout="wide")

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
    .item-label { 
        color: #1E40AF !important; 
        font-size: 15px !important; 
        font-weight: 800 !important; 
        margin-top: 10px !important; 
    }
    </style>
""", unsafe_allow_html=True)

# 驗證機制
if "page_contact_auth" not in st.session_state:
    st.session_state["page_contact_auth"] = False

if not st.session_state["page_contact_auth"]:
    st.write("### 🔒 教師安全驗證專區")
    with st.form("page_auth_form"):
        p = st.text_input("請輸入 5 位數導師密碼：")
        if st.form_submit_button("確認通行"):
            if p.strip() == "12345":
                st.session_state["page_contact_auth"] = True
                st.rerun()
            else:
                st.error("❌ 密碼錯誤。")
    if st.button("⬅️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")
    st.stop()

col_top_title, col_top_back = st.columns([0.80, 0.20])
with col_top_title:
    st.write("# 📝 801 每日聯絡簿與歷史紀錄系統")
with col_top_back: 
    if st.button("🏛️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")

FILE_NAME = "801班_導師班務紀錄總表.xlsx"
TXT_ITEM_FILE = "長期催收清單.txt"
TXT_STATUS_FILE = "長期催收狀態紀錄.txt"

# 完整 27 人名單（包含 9 號與 10 號同名同姓學生）
student_names = [
    "王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", 
    "黃榆涵", "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", 
    "王駿展", "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", 
    "黃楙軒", "董子以", "劉家佑", "魏辰恩"
]
seat_list = [int(i+1) for i in range(len(student_names))]

def get_all_history_dates():
    if not os.path.exists(FILE_NAME): return []
    try:
        with pd.ExcelFile(FILE_NAME, engine="openpyxl") as xl:
            return sorted(xl.sheet_names, reverse=True)
    except: return []

def load_long_term_items():
    if not os.path.exists(TXT_ITEM_FILE): return []
    with open(TXT_ITEM_FILE, "r", encoding="utf-8") as f: 
        return [line.strip() for line in f.readlines() if line.strip()]

def load_long_term_status(items):
    status_dict = {item: {seat: "未繳 ❌" for seat in seat_list} for item in items}
    if not os.path.exists(TXT_STATUS_FILE): return status_dict
    try:
        with open(TXT_STATUS_FILE, "r", encoding="utf-8") as f:
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

def save_long_term_status():
    if "long_term_status" in st.session_state:
        try:
            with open(TXT_STATUS_FILE, "w", encoding="utf-8") as f:
                for item, seats in st.session_state["long_term_status"].items():
                    for seat, status in seats.items(): 
                        f.write(f"{item},{seat},{status}\n")
        except: pass

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
    except: return df_def.copy()

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

tab_daily, tab_history = st.tabs(["📝 每日登記 / 歷史補登", "🔍 歷史總覽與個人查詢"])

long_term_items = load_long_term_items()

if "long_term_status" not in st.session_state:
    st.session_state["long_term_status"] = load_long_term_status(long_term_items)

with tab_daily:
    col_left_panel, col_right_students = st.columns([0.28, 0.72])

    with col_left_panel:
        st.write("### 📅 日期與項目選擇")
        current_date = st.date_input("選擇聯絡簿登記/補登日期：", datetime.now(), key="main_date")
        date_str = current_date.strftime("%Y-%m-%d")
        df_daily = load_daily_data(date_str)
        
        menu_options = ["📝 每日聯絡簿與札記"] + [f"📋 {item}" for item in long_term_items]
        current_view = st.selectbox("🎯 請選擇右側要登記的項目：", menu_options, key="view_selector")

        st.markdown("---")
        new_item = st.text_input("➕ 新增獨立長期催收項目：", placeholder="例如：HPV同意書、註冊費", key="main_item")
        if st.button("確認建立催收項目", use_container_width=True):
            if new_item and new_item not in long_term_items:
                try:
                    with open(TXT_ITEM_FILE, "a", encoding="utf-8") as f: f.write(f"{new_item}\n")
                    st.session_state["long_term_status"][new_item] = {seat: "未繳 ❌" for seat in seat_list}
                    save_long_term_status()
                    st.rerun()
                except: st.error("⚠️ 寫入系統發生衝突，請重試。")

        st.markdown("---")
        st.write("### 📢 即時催繳廣播台")
        
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
        else:
            selected_item_name = current_view.replace("📋 ", "")
            item_status_map = st.session_state["long_term_status"].get(selected_item_name, {})
            unpaid_students = [seat for seat, status in item_status_map.items() if status == "未繳 ❌"]
            
            if unpaid_students:
                t_i = f"【801班 {selected_item_name} 尚未繳交名單】\n"
                for seat in unpaid_students:
                    name = student_names[seat_list.index(seat)]
                    t_i += f"{seat}號 {name}\n"
                st.text_area(f"📋 複製 {selected_item_name} 催繳文字：", value=t_i, height=180, key=f"c_broadcast_{selected_item_name}")
            else: 
                st.success(f"💯 {selected_item_name} 皆已繳齊！")

    with col_right_students:
        if current_view == "📝 每日聯絡簿與札記": 
            st.write(f"### 📅 紀錄登記區：{date_str} 聯絡簿與札記")
        else:
            selected_item_name = current_view.replace("📋 ", "")
            st.write(f"### 📋 長期催收登記區：{selected_item_name}")
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
                        
                        if current_view == "📝 每日聯絡簿與札記":
                            row_s = df_daily[df_daily["座號"] == seat_num].iloc[0]
                            ns = st.radio(f"聯絡簿_{seat_num}", ["已簽 📝", "未簽 ❌"], index=(0 if row_s["聯絡簿簽名"] == "已簽 📝" else 1), horizontal=True, key=f"s_{seat_num}_{date_str}")
                            nd = st.radio(f"札記_{seat_num}", ["已寫 🗒️", "未寫 ❌"], index=(0 if row_s["生活札記"] == "已寫 🗒️" else 1), horizontal=True, key=f"d_{seat_num}_{date_str}")
                            if ns != row_s["聯絡簿簽名"] or nd != row_s["生活札記"]:
                                df_daily.loc[df_daily["座號"] == seat_num, "聯絡簿簽名"], df_daily.loc[df_daily["座號"] == seat_num, "生活札記"] = ns, nd
                                save_daily_data(df_daily, date_str)
                                st.rerun()
                            st.write("✍️ **隨手備註：**")
                            current_memo = "" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])
                            nm = st.text_input(f"備註_{seat_num}", value=current_memo, placeholder="輸入日常備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}")
                            if nm != current_memo:
                                df_daily.loc[df_daily["座號"] == seat_num, "備註事項"] = nm
                                save_daily_data(df_daily, date_str)
                        else:
                            selected_item_name = current_view.replace("📋 ", "")
                            if selected_item_name not in st.session_state["long_term_status"]:
                                st.session_state["long_term_status"][selected_item_name] = {seat: "未繳 ❌" for seat in seat_list}
                            
                            current_status = st.session_state["long_term_status"][selected_item_name].get(seat_num, "未繳 ❌")
                            radio_key = f"r_lt_{selected_item_name}_{seat_num}"
                            
                            # 直接取得勾選的值並比較，若改變立刻存檔並 rerun 刷新左側廣播台
                            new_status = st.radio(
                                f"{selected_item_name}_{seat_num}", 
                                ["已繳 ✅", "未繳 ❌"], 
                                index=(0 if current_status == "已繳 ✅" else 1), 
                                horizontal=True, 
                                key=radio_key, 
                                label_visibility="collapsed"
                            )
                            
                            if new_status != current_status:
                                st.session_state["long_term_status"][selected_item_name][seat_num] = new_status
                                save_long_term_status()
                                st.rerun()

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
            student_options = [f"{seat_list[i]}號 {student_names[i]}" for i in range(len(student_names))]
            selected_student_opt = st.selectbox("選擇學生：", student_options)
            
            if selected_student_opt:
                selected_seat = int(selected_student_opt.split("號")[0])
                student_name = selected_student_opt.split(" ")[1]
                st.write(f"##### 🔎 【{selected_seat}號 {student_name}】歷史全紀錄：")
                
                records = []
                for d in all_dates:
                    df_tmp = load_daily_data(d)
                    row_tmp = df_tmp[df_tmp["座號"] == selected_seat]
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
