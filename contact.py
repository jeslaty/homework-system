import os, pandas as pd, streamlit as st
from datetime import datetime

st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入馬卡龍「淺藍」與「深藍」高對比度美化樣式
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; }
    [data-testid="stSidebar"] { background-color: #E1F5FE !important; }
    h1, h2, h3 { color: #0D47A1 !important; font-weight: 800 !important; font-family: "Noto Sans TC", sans-serif; }
    .stText, p, span, label, div { color: #000000 !important; font-weight: 600 !important; font-size: 16px !important; }
    div[data-testid="stWidgetLabel"] p { color: #000000 !important; font-weight: 700 !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #0D47A1 !important; border-radius: 14px !important;
        background-color: #FFFFFF !important; padding: 16px !important; margin-bottom: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 帳號密碼設定
if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

if not st.session_state["contact_logged_in"]:
    st.title("🔒 歡迎使用 801 導師班務管理系統")
    with st.form("login_form"):
        u, p = st.text_input("教師帳號："), st.text_input("登入密碼：", type="password")
        if st.form_submit_button("確認登入"):
            if u == "Tseng" and p == "12345":
                st.session_state["contact_logged_in"] = True
                st.rerun()
            else: st.error("❌ 帳號或密碼錯誤。")
    st.stop()

# ----------------- 系統主畫面 -----------------
st.title("📝 801聯絡簿管理系統")
current_date = st.sidebar.date_input("📅 選擇登記/查看日期：", datetime.now())
date_str = current_date.strftime("%Y-%m-%d")

if st.sidebar.button("🔒 安全登出"):
    st.session_state["contact_logged_in"] = False
    st.rerun()

FILE_NAME = "801班_導師班務紀錄總表.xlsx"
seats_str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28"
student_names = ["王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", "黃榆涵", "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", "董子以", "劉家佑", "魏辰恩"]
seat_list = [int(x) for x in seats_str.split(",")]

def load_data(target_date):
    df_def = pd.DataFrame({"座號": seat_list, "姓名": student_names, "聯絡簿簽名": "已簽 📝", "生活札記": "已寫 🗒️", "備註事項": ""})
    if not os.path.exists(FILE_NAME):
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w: df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def
    try: return pd.read_excel(FILE_NAME, sheet_name=target_date)
    except:
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def

df = load_data(date_str)

def save_data(updated_df, target_date):
    with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: updated_df.to_excel(w, sheet_name=target_date, index=False)

st.sidebar.markdown("---")
new_item = st.sidebar.text_input("➕ 新增學校催收項目：", placeholder="例如：疫苗施打同意書")
if st.sidebar.button("建立催收欄位"):
    if new_item and new_item not in df.columns:
        df[new_item] = "未繳 ❌"
        save_data(df, date_str)
        st.rerun()

col_main, col_radio = st.columns(2)
with col_main:
    st.subheader(f"📅 日期：{date_str} 紀錄登記")
    extra_items = list(df.columns[5:])
    for i in range(0, len(df), 2):
        g_l, g_r = st.columns(2)
        # 左邊學生
        if i < len(df):
            r_l = df.iloc[i]
            s_l = int(r_l["座號"])
            with g_l.container(border=True):
                st.markdown(f"### 👤 {s_l}號 {r_l['姓名']}")
                c1, c2 = st.columns(2)
                ns_l = c1.radio(f"聯絡簿_{s_l}", ["已簽 📝", "未簽 ❌"], index=["已簽 📝", "未簽 ❌"].index(r_l["聯絡簿簽名"]) if r_l["聯絡簿簽名"] in ["已簽 📝", "未簽 ❌"] else 0, horizontal=True, key=f"s_{s_l}_{date_str}")
                nd_l = c2.radio(f"札記_{s_l}", ["已寫 🗒️", "未寫 ❌"], index=["已寫 🗒️", "未寫 ❌"].index(r_l["生活札記"]) if r_l["生活札記"] in ["已寫 🗒️", "未寫 ❌"] else 0, horizontal=True, key=f"d_{s_l}_{date_str}")
                if ns_l != r_l["聯絡簿簽名"] or nd_l != r_l["生活札記"]:
                    df.loc[df["座號"] == s_l, "聯絡簿簽名"], df.loc[df["座號"] == s_l, "生活札記"] = ns_l, nd_l
                    save_data(df, date_str); st.rerun()
                if extra_items:
                    for item in extra_items:
                        ni_l = st.radio(f"{item}_{s_l}", ["已繳 ✅", "未繳 ❌"], index=["已繳 ✅", "未繳 ❌"].index(r_l[item]) if r_l[item] in ["已繳 ✅", "未繳 ❌"] else 1, horizontal=True, key=f"i_{item}_{s_l}_{date_str}")
                        if ni_l != r_l[item]: df.loc[df["座號"] == s_l, item] = ni_l; save_data(df, date_str); st.rerun()
                nm_l = st.text_input(f"備註_{s_l}", value="" if pd.isna(r_l["備註事項"]) else str(r_l["備註事項"]), placeholder="✍️ 隨手備註...", label_visibility="collapsed", key=f"m_{s_l}_{date_str}")
                if nm_l != ("" if pd.isna(r_l["備註事項"]) else str(r_l["備註事項"])): df.loc[df["座號"] == s_l, "備註事項"] = nm_l; save_data(df, date_str)
        # 右邊學生
        if i + 1 < len(df):
            r_r = df.iloc[i + 1]
            s_r = int(r_r["座號"])
            with g_r.container(border=True):
                st.markdown(f"### 👤 {s_r}號 {r_r['姓名']}")
                c1, c2 = st.columns(2)
                ns_r = c1.radio(f"聯絡簿_{s_r}", ["已簽 📝", "未簽 ❌"], index=["已簽 📝", "未簽 ❌"].index(r_r["聯絡簿簽名"]) if r_r["聯絡簿簽名"] in ["已簽 📝", "未簽 ❌"] else 0, horizontal=True, key=f"s_{s_r}_{date_str}")
                nd_r = c2.radio(f"札記_{s_r}", ["已寫 🗒️", "未寫 ❌"], index=["已寫 🗒️", "未寫 ❌"].index(r_r["生活札記"]) if r_r["生活札記"] in ["已寫 🗒️", "未寫 ❌"] else 0, horizontal=True, key=f"d_{s_r}_{date_str}")
                if ns_r != r_r["聯絡簿簽名"] or nd_r != r_r["生活札記"]:
                    df.loc[df["座號"] == s_r, "聯絡簿簽名"], df.loc[df["座號"] == s_r, "生活札記"] = ns_r, nd_r
                    save_data(df, date_str); st.rerun()
                if extra_items:
                    for item in extra_items:
                        ni_r = st.radio(f"{item}_{s_r}", ["已繳 ✅", "未繳 ❌"], index=["已繳 ✅", "未繳 ❌"].index(r_r[item]) if r_r[item] in ["已繳 ✅", "未繳 ❌"] else 1, horizontal=True, key=f"i_{item}_{s_r}_{date_str}")
                        if ni_r != r_r[item]: df.loc[df["座號"] == s_r, item] = ni_r; save_data(df, date_str); st.rerun()
                nm_r = st.text_input(f"備註_{s_r}", value="" if pd.isna(r_r["備註事項"]) else str(r_r["備註事項"]), placeholder="✍️ 隨手備註...", label_visibility="collapsed", key=f"m_{s_r}_{date_str}")
                if nm_r != ("" if pd.isna(r_r["備註事項"]) else str(r_r["備註事項"])): df.loc[df["座號"] == s_r, "備註事項"] = nm_r; save_data(df, date_str)

with col_radio:
    st.subheader(f"📢 {date_str} 即時催繳廣播台")
    # A. 聯絡簿
    df_ns = df[df["聯絡簿簽名"] == "未簽 ❌"]
    if not df_ns.empty:
        t = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
        st.text_area("📋 複製傳至家長群組：", value=t, height=120, key="c_s")
    else: st.success("🎉 本日聯絡簿全班皆已簽名！")
    # B. 札記
    df_nd = df[df["生活札記"] == "未寫 ❌"]
    if not df_nd.empty:
        t = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
        st.text_area("📋 複製傳至班級群組：", value=t, height=120, key="c_d")
    # C. 自訂項目
    if extra_items:
        st.markdown("---")
        for item in extra_items:
            df_ni = df[df[item] == "未繳 ❌"]
            if not df_ni.empty:
                t = f"【801班 {item} 尚未繳交名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ni.iterrows()])
                st.text_area(f"📋 複製 {item} 催繳文字：", value=t, height=120, key=f"c_{item}")
            else: st.success(f"💯 {item} 全班皆已繳齊！")

st.markdown("---")
st.subheader(f"📊 801班 {date_str} 綜合班務總表（唯讀檢視）")
st.dataframe(df, use_container_width=True)
