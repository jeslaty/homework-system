import os
from datetime import datetime
import pandas as pd
import streamlit as st

# 設定網頁標題與圖示
st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入馬卡龍淡綠、淡黃色美化（導師溫馨風格）
st.markdown(
    """
    <style>
    .stApp { background-color: #F0F9F4 !important; }
    [data-testid="stSidebar"] { background-color: #FFFDE6 !important; }
    h1, h2, h3 { color: #4A4A4A !important; font-family: "Helvetica Neue", Arial, "Noto Sans TC", sans-serif; }
    .stText, p, span, label { color: #333333 !important; }
    
    /* 🍏 強制讓原生的 st.container 顯示出明顯的馬卡龍綠框框 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #CDE7D7 !important;
        border-radius: 12px !important;
        background-color: #F7FDF9 !important;
        padding: 12px !important;
        margin-bottom: 8px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 🔑 帳號密碼設定
USER_USERNAME = "Tseng"
USER_PASSWORD = "12345"

if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

# ----------------- 登入畫面 -----------------
if not st.session_state["contact_logged_in"]:
    st.title("🔒 歡迎使用 801 導師班務管理系統")
    with st.form("login_form"):
        input_username = st.text_input("教師帳號：")
        input_password = st.text_input("登入密碼：", type="password")
        submit_button = st.form_submit_button("確認登入")
        if submit_button:
            if input_username == USER_USERNAME and input_password == USER_PASSWORD:
                st.session_state["contact_logged_in"] = True
                st.success("🎉 登入成功！")
                st.rerun()
            else:
                st.error("❌ 帳號或密碼錯誤。")
    st.stop()

# ----------------- 系統主畫面 (登入後) -----------------
st.title("📝 801聯絡簿管理系統")

# 📅 日期選擇功能（左側邊欄最上方）
st.sidebar.header("📅 日期切換")
current_date = st.sidebar.date_input("選擇登記/查看日期：", datetime.now())
date_str = current_date.strftime("%Y-%m-%d")

if st.sidebar.button("🔒 安全登出"):
    st.session_state["contact_logged_in"] = False
    st.rerun()

FILE_NAME = "801班_導師班務紀錄總表.xlsx"

# 801班真實名單
seats_str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28"
student_names = [
    "王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", "黃榆涵", "黃榆涵",
    "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", "吳軒佑", "李宇哲", "林柏辰",
    "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", "董子以", "劉家佑", "魏辰恩"
]
seat_list = [int(x) for x in seats_str.split(",")]


# 初始化 Excel 檔案
def load_data(target_date):
    default_df = pd.DataFrame(
        {
            "座號": seat_list,
            "姓名": student_names,
            "聯絡簿簽名": "已簽 📝",
            "生活札記": "已寫 🗒️",
            "備註事項": "",
        }
    )

    if not os.path.exists(FILE_NAME):
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as writer:
            default_df.to_excel(writer, sheet_name=target_date, index=False)
        return default_df
    else:
        try:
            return pd.read_excel(FILE_NAME, sheet_name=target_date)
        except Exception:
            with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                default_df.to_excel(writer, sheet_name=target_date, index=False)
            return default_df


df = load_data(date_str)


# 儲存資料
def save_data(updated_df, target_date):
    with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        updated_df.to_excel(writer, sheet_name=target_date, index=False)


# ⚙️ 左側邊欄：新增學校催收項目
st.sidebar.markdown("---")
st.sidebar.subheader("➕ 新增學校催收項目")
st.sidebar.caption("💡 新增項目會套用在「當天」的紀錄中")
new_item = st.sidebar.text_input("輸入項目名稱：", placeholder="例如：疫苗施打同意書")
if st.sidebar.button("建立催收欄位"):
    if new_item:
        if new_item in df.columns:
            st.sidebar.error("⚠️ 該項目已存在！")
        else:
            df[new_item] = "未繳 ❌"
            save_data(df, date_str)
            st.sidebar.success(f"✅ 已成功新增：{new_item}")
            st.rerun()
    else:
        st.sidebar.warning("⚠️ 請輸入項目名稱")

# 主畫面配置：左邊大欄放學生紀錄（佔65%），右邊小欄放廣播台（佔35%）
col_main, col_radio_station = st.columns([13, 7])

with col_main:
    st.subheader(f"📅 日期：{date_str} 紀錄登記")
    st.caption("點選狀態後會即時存檔。左右各一位學生，減少滾動畫面。")
    st.write("")

    extra_items = list(df.columns[5:])

    # 🔄 兩兩一組，產生左右並排的學生
    for i in range(0, len(df), 2):
        # 建立左右兩欄放兩個學生
        grid_left, grid_right = st.columns(2)

        # ---- 左邊學生 ----
        if i < len(df):
            row_l = df.iloc[i]
            seat_l = int(row_l["座號"])
            name_l = row_l["姓名"]

            with grid_left.container(border=True): # 原生實線框
                st.markdown(f"**👤 {seat_l}號 {name_l}**")
                
                c1, c2 = st.columns(2)
                current_sign_l = row_l["聯絡簿簽名"]
                sign_opts = ["已簽 📝", "未簽 ❌"]
                s_idx = sign_opts.index(current_sign_l) if current_sign_l in sign_opts else 0
                new_sign_l = c1.radio(f"聯絡簿_{seat_l}", sign_opts, index=s_idx, horizontal=True, key=f"sign_{seat_l}_{date_str}")
                if new_sign_l != current_sign_l:
                    df.loc[df["座號"] == seat_l, "聯絡簿簽名"] = new_sign_l
                    save_data(df, date_str)
                    st.rerun()

                current_diary_l = row_l["生活札記"]
                diary_opts = ["已寫 🗒️", "未寫 ❌"]
                d_idx = diary_opts.index(current_diary_l) if current_diary_l in diary_opts else 0
                new_diary_l = c2.radio(f"札記_{seat_l}", diary_opts, index=d_idx, horizontal=True, key=f"diary_{seat_l}_{date_str}")
                if new_diary_l != current_diary_l:
                    df.loc[df["座號"] == seat_l, "生活札記"] = new_diary_l
                    save_data(df, date_str)
                    st.rerun()

                if extra_items:
                    for item in extra_items:
                        current_item_l = row_l[item]
                        item_opts = ["已繳 ✅", "未繳 ❌"]
                        i_idx = item_opts.index(current_item_l) if current_item_l in item_opts else 1
                        st.markdown(f"💼 *{item}*")
                        new_item_l = st.radio(f"{item}_{seat_l}_{date_str}", item_opts, index=i_idx, horizontal=True, key=f"item_{item}_{seat_l}_{date_str}", label_visibility="collapsed")
                        if new_item_l != current_item_l:
                            df.loc[df["座號"] == seat_l, item] = new_item_l
                            save_data(df, date_str)
                            st.rerun()

                current_memo_l = "" if pd.isna(row_l["備註事項"]) else str(row_l["備註事項"])
                new_memo_l = st.text_input(f"備註_{seat_l}_{date_str}", value=current_memo_l, placeholder="✍️ 隨手備註", label_visibility="collapsed", key=f"memo_{seat_l}_{date_str}")
                if new_memo_l != current_memo_l:
                    df.loc[df["座號"] == seat_l, "備註事項"] = new_memo_l
                    save_data(df, date_str)

        # ---- 右邊學生 ----
        if i + 1 < len(df):
            row_r = df.iloc[i + 1]
            seat_r = int(row_r["座號"])
            name_r = row_r["姓名"]

            with grid_right.container(border=True): # 原生實線框
                st.markdown(f"**👤 {seat_r}號 {name_r}**")
                
                c1, c2 = st.columns(2)
                current_sign_r = row_r["聯絡簿簽名"]
                s_idx = sign_opts.index(current_sign_r) if current_sign_r in sign_opts else 0
                new_sign_r = c1.radio(f"聯絡簿_{seat_r}", sign_opts, index=s_idx, horizontal=True, key=f"sign_{seat_r}_{date_str}")
                if new_sign_r != current_sign_r:
                    df.loc[df["座號"] == seat_r, "聯絡簿簽名"] = new_sign_r
                    save_data(df, date_str)
                    st.rerun()

                current_diary_r = row_r["生活札記"]
                d_idx = diary_opts.index(current_diary_r) if current_diary_r in diary_opts else 0
                new_diary_r = c2.radio(f"札記_{seat_r}", diary_opts, index=d_idx, horizontal=True, key=f"diary_{seat_r}_{date_str}")
                if new_diary_r != current_diary_r:
                    df.loc[df["座號"] == seat_r, "生活札記"] = new_diary_r
                    save_data(df, date_str)
                    st.rerun()

                if extra_items:
                    for item in extra_items:
                        current_item_r = row_r[item]
                        item_opts = ["已繳 ✅", "未繳 ❌"]
                        i_idx = item_opts.index(current_item_r) if current_item_r in item_opts else 1
                        st.markdown(f"💼 *{item}*")
                        new_item_r = st.radio(f"{item}_{seat_r}_{date_str}", item_opts, index=i_idx, horizontal=True, key=f"item_{item}_{seat_r}_{date_str}", label_visibility="collapsed")
                        if new_item_r != current_item_r:
                            df.loc[df["座號"] == seat_r, item] = new_item_r
                            save_data(df, date_str)
                            st.rerun()

                current_memo_r = "" if pd.isna(row_r["備註事項"]) else str(row_r["備註事項"])
                new_memo_r = st.text_input(f"備註_{seat_r}_{date_str}", value=current_memo_r, placeholder="✍️ 隨手備註", label_visibility="collapsed", key=f"memo_{seat_r}_{date_str}")
                if new_memo_r != current_memo_r:
                    df.loc[df["座號"] == seat_r, "備註事項"] = new_memo_r
                    save_data(df, date_str)

with col_radio_station:
    st.subheader(f"📢 {date_str} 即時催繳廣播台")
    st.write("")

    # A. 聯絡簿未簽名名單
    no_sign_df = df[df["聯絡簿簽名"] == "未簽 ❌"]
    if not no_sign_df.empty:
        st.error(f"❌ 本日聯絡簿未簽名 ({len(no_sign_df)} 人)：")
        sign_text = f"【801班 {date_str} 聯絡簿未簽催簽名單】\n"
        for _, row in no_sign_df.iterrows():
            sign_text += f"{int(row['座號'])}號 {row['姓名']}\n"
        st.text_area("可複製傳至家長群組：", value=sign_text, height=120, key=f"copy_sign_{date_str}")
    else:
        st.success("🎉 本日聯絡簿全班皆已簽名！")

    # B. 札記未寫名單
    no_diary_df = df[df["生活札記"] == "未寫 ❌"]
