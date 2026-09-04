import os
from datetime import datetime
import pandas as pd
import streamlit as st

# 設定網頁標題與圖示
st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入馬卡龍淡綠、淡黃色美化，並新增「學生獨立卡片框」的樣式
st.markdown(
    """
    <style>
    /* 全局背景：馬卡龍淡綠 */
    .stApp { background-color: #F0F9F4 !important; }
    /* 左側邊欄：馬卡龍淡黃 */
    [data-testid="stSidebar"] { background-color: #FFFDE6 !important; }
    h1, h2, h3 { color: #4A4A4A !important; font-family: "Helvetica Neue", Arial, "Noto Sans TC", sans-serif; }
    .stText, p, span, label { color: #333333 !important; }
    
    /* 🍏 學生專屬的卡片框框樣式 */
    .student-card {
        background-color: #F7FDF9 !important; /* 框框內用極淡的馬卡龍綠 */
        border: 1px solid #CDE7D7 !important; /* 馬卡龍綠邊框 */
        border-radius: 12px !important;       /* 溫柔的圓角 */
        padding: 16px !important;             /* 留白內距，不擁擠 */
        margin-bottom: 16px !important;        /* 框與框之間的距離 */
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important; /* 微微的陰影，更有質感 */
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 🔑 帳號密碼設定
USER_USERNAME = "teacher"
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

# 主畫面配置
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📅 日期：{date_str} 紀錄登記")
    st.caption("點選狀態後，系統會即時自動同步存檔至雲端 Excel")
    st.write("")

    # 透過迴圈，幫每個學生產生點選紀錄卡片
    for index, row in df.iterrows():
        seat = int(row["座號"])
        name = row["姓名"]

        # 使用 Streamlit 的 container 並結合外圍 HTML 語法建立精美框框
        with st.container():
            st.markdown(f'<div class="student-card">', unsafe_allow_html=True)
            st.markdown(f"📊 **{seat}號 {name}**")

            extra_items = list(df.columns[5:])

            # 1. 聯絡簿與札記單行配置
            c1, c2 = st.columns(2)

            current_sign = row["聯絡簿簽名"]
            sign_opts = ["已簽 📝", "未簽 ❌"]
            s_idx = sign_opts.index(current_sign) if current_sign in sign_opts else 0
            new_sign = c1.radio(
                f"聯絡簿_{seat}", sign_opts, index=s_idx, horizontal=True, key=f"sign_{seat}_{date_str}"
            )
            if new_sign != current_sign:
                df.loc[df["座號"] == seat, "聯絡簿簽名"] = new_sign
                save_data(df, date_str)
                st.rerun()

            current_diary = row["生活札記"]
            diary_opts = ["已寫 🗒️", "未寫 ❌"]
            d_idx = diary_opts.index(current_diary) if current_diary in diary_opts else 0
            new_diary = c2.radio(
                f"札記_{seat}", diary_opts, index=d_idx, horizontal=True, key=f"diary_{seat}_{date_str}"
            )
            if new_diary != current_diary:
                df.loc[df["座號"] == seat, "生活札記"] = new_diary
                save_data(df, date_str)
                st.rerun()

            # 2. 學校自訂收發項目登記
            if extra_items:
                for item in extra_items:
                    current_item_status = row[item]
                    item_opts = ["已繳 ✅", "未繳 ❌"]
                    i_idx = item_opts.index(current_item_status) if current_item_status in item_opts else 1

                    st.markdown(f"📋 **學校收發：{item}**")
                    new_item_status = st.radio(
                        f"{item}_{seat}_{date_str}",
                        item_opts,
                        index=i_idx,
                        horizontal=True,
                        key=f"item_{item}_{seat}_{date_str}",
                        label_visibility="collapsed",
                    )
                    if new_item_status != current_item_status:
                        df.loc[df["座號"] == seat, item] = new_item_status
                        save_data(df, date_str)
                        st.rerun()

            # 3. 隨手備註事項
            current_memo = "" if pd.isna(row["備註事項"]) else str(row["備註事項"])
            new_memo = st.text_input(
                f"備註_{seat}_{date_str}",
                value=current_memo,
                placeholder="✍️ 常規紀錄/請假/特殊狀況備註",
                label_visibility="collapsed",
                key=f"memo_{seat}_{date_str}",
            )
            if new_memo != current_memo:
                df.loc[df["座號"] == seat, "備註事項"] = new_memo
                save_data(df, date_str)

            st.markdown('</div>', unsafe_allow_html=True)  # 結束卡片框框

with col2:
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
    if not no_diary_df.empty:
        st.warning(f"❌ 本日隨筆札記未完成 ({len(no_diary_df)} 人)：")
        diary_text = f"【801班 {date_str} 札記未完成催收名單】\n"
        for _, row in no_diary_df.iterrows():
            diary_text += f"{int(row['座號'])}號 {row['姓名']}\n"
        st.text_area("可複製傳至班級群組：", value=diary_text, height=120, key=f"copy_diary_{date_str}")

    # C. 學校各類項目未繳名單
    extra_items = list(df.columns[5:])
    if extra_items:
        st.markdown("---")
        for item in extra_items:
            no_item_df = df[df[item] == "未繳 ❌"]
            if not no_item_df.empty:
                st.info(f"📌 {item} 尚未繳交 ({len(no_item_df)} 人)：")
                item_text = f"【801班 {item} 尚未繳交名單】\n"
                for _, row in no_item_df.iterrows():
                    item_text += f"{int(row['座號'])}號 {row['姓名']}\n"
                st.text_area(f"複製 {item} 催繳文字：", value=item_text, height=120, key=f"copy_{item}_{date_str}")
            else:
                st.success(f"💯 {item} 全班皆已繳齊！")

# 底部檢視總表
st.markdown("---")
st.subheader(f"📊 801班 {date_str} 綜合班務總表（唯讀檢視）")
st.dataframe(df, use_container_width=True)
