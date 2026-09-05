import os
import pandas as pd
import streamlit as st
from datetime import datetime

# 1. 頁面基本設定
st.set_page_config(page_title="01_每日聯絡簿管理", page_icon="📝", layout="wide")

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

# 2. 判斷是否從主控台傳入免密碼驗證參數
if st.query_params.get("auth") == "passed":
    st.session_state["page_contact_auth"] = True

if "page_contact_auth" not in st.session_state:
    st.session_state["page_contact_auth"] = False

# 權限驗證區
if not st.session_state["page_contact_auth"]:
    st.write("### 🔒 教師安全驗證專區（此頁首次開啟需驗證）")
    with st.form("page_auth_form"):
        p = st.text_input("請輸入 5 位數導師密碼：", type="password")
        if st.form_submit_button("確認通行"):
            if p.strip() == "12345":
                st.session_state["page_contact_auth"] = True
                st.rerun()
            else:
                st.error("❌ 密碼錯誤。")
    if st.button("⬅️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")
    st.stop()

# 3. 頁面頂部標題與返回按鈕
col_top_title, col_top_back = st.columns([0.82, 0.18])
with col_top_title:
    st.write("# 📝 801每日聯絡簿管理系統")
with col_top_back: 
    if st.button("🏛️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")

# 4. 基礎資料與名單設定
FILE_NAME = "801班_導師班務紀錄總表.xlsx"
TXT_ITEM_FILE = "長期催收清單.txt"
TXT_STATUS_FILE = "長期催收狀態紀錄.txt"

STUDENT_NAMES = [
    "王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", 
    "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", 
    "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", 
    "董子以", "劉家佑", "魏辰恩"
]
SEAT_LIST = list(range(1, len(STUDENT_NAMES) + 1))

# 5. 檔案讀寫邏輯 (包含防損毀與自動修復機制)
def load_long_term_items():
    if not os.path.exists(TXT_ITEM_FILE):
        return []
    with open(TXT_ITEM_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_long_term_item(item_name):
    items = load_long_term_items()
    if item_name not in items:
        with open(TXT_ITEM_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item_name}\n")

def load_long_term_status(items):
    status_dict = {item: {seat: "未繳 ❌" for seat in SEAT_LIST} for item in items}
    if not os.path.exists(TXT_STATUS_FILE):
        return status_dict
    try:
        with open(TXT_STATUS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    item, seat_str, status = parts
                    seat_num = int(seat_str)
                    if item in status_dict and seat_num in status_dict[item]:
                        status_dict[item][seat_num] = status
    except Exception:
        pass
    return status_dict

def save_long_term_status(status_dict):
    try:
        with open(TXT_STATUS_FILE, "w", encoding="utf-8") as f:
            for item, seats in status_dict.items():
                for seat, status in seats.items():
                    f.write(f"{item},{seat},{status}\n")
    except Exception as e:
        st.error(f"儲存狀態失敗: {e}")

def load_daily_data(target_date):
    df_def = pd.DataFrame({
        "座號": SEAT_LIST,
        "姓名": STUDENT_NAMES,
        "聯絡簿簽名": "已簽 📝",
        "生活札記": "已寫 🗒️",
        "備註事項": ""
    })
    
    if not os.path.exists(FILE_NAME):
        try:
            with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
                df_def.to_excel(w, sheet_name=target_date, index=False)
        except Exception:
            pass
        return df_def

    try:
        with pd.ExcelFile(FILE_NAME, engine="openpyxl") as xl:
            if target_date in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=target_date)
                df["備註事項"] = df["備註事項"].fillna("")
                return df
            else:
                return df_def.copy()
    except Exception:
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
            df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def

def save_daily_data(updated_df, target_date):
    sheets_data = {}
    if os.path.exists(FILE_NAME):
        try:
            with pd.ExcelFile(FILE_NAME, engine="openpyxl") as xl:
                for sheet in xl.sheet_names:
                    if sheet != target_date:
                        sheets_data[sheet] = pd.read_excel(xl, sheet_name=sheet)
        except Exception:
            sheets_data = {}

    sheets_data[target_date] = updated_df

    try:
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
            for sheet, s_df in sheets_data.items():
                s_df.to_excel(w, sheet_name=sheet, index=False)
    except Exception as e:
        st.error(f"寫入失敗: {e}")

# 6. 初始化資料狀態
long_term_items = load_long_term_items()
long_term_status = load_long_term_status(long_term_items)

# 7. 畫面佈局
col_left_panel, col_right_students = st.columns([0.28, 0.72])

with col_left_panel:
    st.write("### 📅 班務管理與項目切換")
    current_date = st.date_input("選擇聯絡簿登記日期：", datetime.now(), key="main_date")
    date_str = current_date.strftime("%Y-%m-%d")
    
    df_daily = load_daily_data(date_str)
    
    menu_options = ["📝 每日聯絡簿與札記"] + [f"📋 {item}" for item in long_term_items]
    current_view = st.selectbox("🎯 請選擇右側要登記的項目：", menu_options, key="view_selector")

    st.markdown("---")
    new_item = st.text_input("➕ 新增獨立長期催收項目：", placeholder="例如：HPV同意書、註冊費", key="main_item")
    if st.button("確認建立催收項目", use_container_width=True):
        if new_item.strip():
            if new_item.strip() not in long_term_items:
                save_long_term_item(new_item.strip())
                st.success(f"已建立：{new_item.strip()}")
                st.rerun()
            else:
                st.warning("此項目已存在。")

    st.markdown("---")
    st.write("### 📢 即時催繳廣播台")
    
    if current_view == "📝 每日聯絡簿與札記":
        df_ns = df_daily[df_daily["聯絡簿簽名"] == "未簽 ❌"]
        if not df_ns.empty:
            t_s = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
            st.text_area("📋 複製傳至家長群組：", value=t_s, height=120, key="c_s")
        else:
            st.success("🎉 本日聯絡簿全班皆已簽名！")

        df_nd = df_daily[df_daily["生活札記"] == "未寫 ❌"]
        if not df_nd.empty:
            t_d = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
            st.text_area("📋 複製傳至班級群組：", value=t_d, height=120, key="c_d")
        else:
            st.success("🎉 本日生活札記全班皆已完成！")
    else:
        selected_item_name = current_view.replace("📋 ", "")
        unpaid_students = [seat for seat, status in long_term_status.get(selected_item_name, {}).items() if status == "未繳 ❌"]
        if unpaid_students:
            t_i = f"【801班 {selected_item_name} 尚未繳交名單】\n"
            for seat in unpaid_students:
                name = STUDENT_NAMES[SEAT_LIST.index(seat)]
                t_i += f"{seat}號 {name}\n"
            st.text_area(f"📋 複製 {selected_item_name} 催繳文字：", value=t_i, height=150, key=f"c_final_{selected_item_name}")
        else:
            st.success(f"💯 {selected_item_name} 皆已繳齊！")

with col_right_students:
    if current_view == "📝 每日聯絡簿與札記":
        st.write(f"### 📅 紀錄登記區：{date_str} 聯絡簿與札記")
    else:
        selected_item_name = current_view.replace("📋 ", "")
        st.write(f"### 📋 長期催收登記區：{selected_item_name}")
    st.write("")

    for i in range(0, len(STUDENT_NAMES), 4):
        grid = st.columns(4)
        for idx_grid in range(4):
            student_idx = i + idx_grid
            if student_idx < len(STUDENT_NAMES):
                seat_num = SEAT_LIST[student_idx]
                name_s = STUDENT_NAMES[student_idx]
                gender_icon = "🌸" if seat_num <= 14 else "🍀"
                
                with grid[idx_grid].container(border=True):
                    st.markdown(f'### <span style="white-space:nowrap;">{gender_icon} {seat_num}號 {name_s}</span>', unsafe_allow_html=True)
                    st.write("")
                    
                    if current_view == "📝 每日聯絡簿與札記":
                        row_s = df_daily[df_daily["座號"] == seat_num].iloc[0]
                        
                        ns = st.radio(
                            f"聯絡簿_{seat_num}", 
                            ["已簽 📝", "未簽 ❌"], 
                            index=(0 if row_s["聯絡簿簽名"] == "已簽 📝" else 1), 
                            horizontal=True, 
                            key=f"s_{seat_num}_{date_str}"
                        )
                        nd = st.radio(
                            f"札記_{seat_num}", 
                            ["已寫 🗒️", "未寫 ❌"], 
                            index=(0 if row_s["生活札記"] == "已寫 🗒️" else 1), 
                            horizontal=True, 
                            key=f"d_{seat_num}_{date_str}"
                        )
                        
                        if ns != row_s["聯絡簿簽名"] or nd != row_s["生活札記"]:
                            df_daily.loc[df_daily["座號"] == seat_num, "聯絡簿簽名"] = ns
                            df_daily.loc[df_daily["座號"] == seat_num, "生活札記"] = nd
                            save_daily_data(df_daily, date_str)
                            st.rerun()
                            
                        st.write("✍️ **隨手備註：**")
                        current_memo = str(row_s["備註事項"]) if pd.notna(row_s["備註事項"]) else ""
                        nm = st.text_input(
                            f"備註_{seat_num}", 
                            value=current_memo, 
                            placeholder="輸入日常備註...", 
                            label_visibility="collapsed", 
                            key=f"m_{seat_num}_{date_str}"
                        )
                        if nm != current_memo:
                            df_daily.loc[df_daily["座號"] == seat_num, "備註事項"] = nm
                            save_daily_data(df_daily, date_str)
                    else:
                        selected_item_name = current_view.replace("📋 ", "")
                        current_status = long_term_status[selected_item_name].get(seat_num, "未繳 ❌")
                        
                        ni = st.radio(
                            f"{selected_item_name}_{seat_num}", 
                            ["已繳 ✅", "未繳 ❌"], 
                            index=(0 if current_status == "已繳 ✅" else 1), 
                            horizontal=True, 
                            key=f"lt_{selected_item_name}_{seat_num}", 
                            label_visibility="collapsed"
                        )
                        if ni != current_status:
                            long_term_status[selected_item_name][seat_num] = ni
                            save_long_term_status(long_term_status)
                            st.rerun()

st.markdown("---")
if current_view == "📝 每日聯絡簿與札記":
    st.markdown(f"### 📊 801班 {date_str} 每日聯絡簿總表（唯讀檢視）")
    st.dataframe(df_daily, use_container_width=True)
