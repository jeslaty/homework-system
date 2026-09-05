import os, pandas as pd, streamlit as st
from datetime import datetime

st.set_page_config(page_title="01_每日聯絡簿管理", page_icon="📝", layout="wide")

# 🎨 注入全站字體優化、且【徹底物理性消滅本頁左側灰色選單、隱藏原廠頂部空白欄】最高優先權指令
st.markdown("""
    <style>
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif !important;
    }
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="stSidebarContent"],
    button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"], #MainMenu, header[data-testid="stHeader"] { 
        display: none !important; visibility: hidden !important; width: 0px !important; height: 0px !important;
    }
    .item-label { color: #1E40AF !important; font-size: 15px !important; font-weight: 800 !important; margin-top: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# 🎯【免頻繁登入保持鎖】只要大廳登入過，全站維持永久安全通行
if "contact_logged_in" not in st.session_state or not st.session_state["contact_logged_in"]:
    st.error("🔒 安全提示：請先回到主控台首頁進行教師身分登入。")
    if st.button("⬅️ 返回主控台登入頁面", use_container_width=True): st.switch_page("main.py")
    st.stop()

col_top_title, col_top_back = st.columns([0.82, 0.18])
with col_top_title: st.write("# 📝 801每日聯絡簿管理網頁")
with col_top_back: 
    if st.button("🏛️ 返回管理主控台", use_container_width=True): st.switch_page("main.py")

FILE_NAME = "801班_導師班務紀錄總表.xlsx"
seats_str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28"
student_names = ["王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", "黃榆涵", "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", "吳軒佑", "李宇哲", "林柏辰", "魏辰恩", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", "董子以", "劉家佑", "魏辰恩"]
seat_list = [int(x) for x in seats_str.split(",")]

# 🚀 終極修復：鋼筋水泥級 Excel 跨日期自動尋軌安全防護網
def load_data(target_date):
    df_def = pd.DataFrame({"座號": seat_list, "姓名": student_names, "聯絡簿簽名": "已簽 📝", "生活札記": "已寫 🗒️", "備註事項": ""})
    
    # 🕵️ 安全探索全域已存在的長期催收項目
    global_extra_cols = []
    if os.path.exists(FILE_NAME):
        try:
            with pd.ExcelFile(FILE_NAME) as xl:
                for sheet in xl.sheet_names:
                    sheet_df = pd.read_excel(FILE_NAME, sheet_name=sheet)
                    for col in sheet_df.columns[5:]:
                        if col not in global_extra_cols: global_extra_cols.append(col)
        except: pass

    # 🛠️ 情況 A：如果檔案不存在，一秒直接初始化新檔案
    if not os.path.exists(FILE_NAME):
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w: df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def
        
    # 🛠️ 情況 B：檔案存在，安全讀取或補充分頁
    try:
        with pd.ExcelFile(FILE_NAME) as xl:
            if target_date in xl.sheet_names:
                df_current = pd.read_excel(FILE_NAME, sheet_name=target_date)
            else:
                df_current = df_def.copy()
                
        # 🎯 跨日同步：將別的日期建立的項目，100% 同步追加到今天，達成長期獨立追蹤！
        for col in global_extra_cols:
            if col not in df_current.columns: df_current[col] = "未繳 ❌"
        return df_current
    except:
        return df_def

col_left_panel, col_right_students = st.columns([0.25, 0.75])

with col_left_panel:
    st.write("### 📅 班務管理與切換")
    current_date = st.date_input("選擇登記/查看日期：", datetime.now(), key="main_date")
    date_str = current_date.strftime("%Y-%m-%d")
    df = load_data(date_str)
    extra_items = list(df.columns[5:])
    
    def save_data(updated_df, target_date):
        try:
            sheets_data = {}
            if os.path.exists(FILE_NAME):
                with pd.ExcelFile(FILE_NAME) as xl:
                    for sheet in xl.sheet_names: sheets_data[sheet] = pd.read_excel(FILE_NAME, sheet_name=sheet)
            sheets_data[target_date] = updated_df
            with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
                for sheet, s_df in sheets_data.items(): s_df.to_excel(w, sheet_name=sheet, index=False)
        except: st.error("⚠️ Excel 檔案寫入暫時衝突，請稍後重試。")

    new_item = st.text_input("➕ 新增獨立跨日催收項目：", placeholder="例如：疫苗施打同意書", key="main_item")
    if st.button("建立長期催收欄位", use_container_width=True):
        if new_item and new_item not in df.columns:
            df[new_item] = "未繳 ❌"
            save_data(df, date_str); st.rerun()

    st.markdown("---")
    st.write(f"### 📢 {date_str} 即時催繳廣播台")
    
    df_ns = df[df["聯絡簿簽名"] == "未簽 ❌"]
    if not df_ns.empty:
        t_s = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
        st.text_area("📋 複製傳至家長群組：", value=t_s, height=120, key="c_s")
    else: st.success("🎉 本日聯絡簿全班皆已簽名！")

    df_nd = df[df["生活札記"] == "未寫 ❌"]
    if not df_nd.empty:
        t_d = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
        st.text_area("📋 複製傳至班級群組：", value=t_d, height=120, key="c_d")

    if extra_items:
        st.markdown("---")
        for item in extra_items:
            df_ni = df[df[item] == "未繳 ❌"]
            if not df_ni.empty:
                t_i = f"【801班 {item} 尚未繳交名單】\n" + "".join([f"{int(r['造號'] if '造號' in r else r['座號'])}號 {r['姓名']}\n" for _, r in df_ni.iterrows()])
                st.text_area(f"📋 複製 {item} 催繳文字：", value=t_i, height=120, key=f"c_{item}")
            else: st.success(f"💯 {item} 皆已繳齊！")

with col_right_students:
    st.write("### 📅 紀錄登記區")
    st.write("")

    for i in range(0, len(df), 4):
        grid = st.columns(4)
        for idx_grid in range(4):
            student_idx = i + idx_grid
            if student_idx < len(df):
                row_s = df.iloc[student_idx]
                seat_num = int(row_s["座號"])
                name_s = row_s["姓名"]
                gender_icon = "🌸" if seat_num <= 15 else "🍀"
                
                with grid[idx_grid].container(border=True):
                    if seat_num <= 15:
                        st.markdown(f'<div style="background-color:#FFF1F2;border:2.5px solid #E11D48;border-radius:10px;padding:8px;text-align:center;"><span style="color:#991B1B;font-size:20px;font-weight:900;white-space:nowrap;">{gender_icon} {seat_num}號 {name_s}</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="background-color:#F0F7FF;border:2.5px solid #2563EB;border-radius:10px;padding:8px;text-align:center;"><span style="color:#1E40AF;font-size:20px;font-weight:900;white-space:nowrap;">{gender_icon} {seat_num}號 {name_s}</span></div>', unsafe_allow_html=True)
                    st.write("")
                    
                    ns = st.radio(f"聯絡簿_{seat_num}", ["已簽 📝", "未簽 ❌"], index=(0 if row_s["聯絡簿簽名"] == "已簽 📝" else 1), horizontal=True, key=f"s_{seat_num}_{date_str}")
                    nd = st.radio(f"札記_{seat_num}", ["已寫 🗒️", "未寫 ❌"], index=(0 if row_s["生活札記"] == "已寫 🗒️" else 1), horizontal=True, key=f"d_{seat_num}_{date_str}")
                    
                    if ns != row_s["聯絡簿簽名"] or nd != row_s["生活札記"]:
                        df.loc[df["座號"] == seat_num, "聯絡簿簽名"], df.loc[df["座號"] == seat_num, "生活札記"] = ns, nd
                        save_data(df, date_str); st.rerun()
                    
                    if extra_items:
                        for item in extra_items:
                            st.markdown(f'<div class="item-label">📋 長期催收：{item}</div>', unsafe_allow_html=True)
                            ni = st.radio(f"{item}_{seat_num}", ["已繳 ✅", "未繳 ❌"], index=(0 if row_s[item] == "已繳 ✅" else 1), horizontal=True, key=f"i_{item}_{seat_num}_{date_str}", label_visibility="collapsed")
                            if ni != row_s[item]:
                                df.loc[df["座號"] == seat_num, item] = ni
                                # 🎯 鋼筋水泥級跨日寫入：將繳交進度 100% 同步覆蓋到 Excel 的所有分頁中，永久連動！
                                try:
                                    sheets_data = {}
                                    if os.path.exists(FILE_NAME):
                                        with pd.ExcelFile(FILE_NAME) as xl:
                                            for sheet in xl.sheet_names:
                                                s_df = pd.read_excel(FILE_NAME, sheet_name=sheet)
                                                if item not in s_df.columns: s_df[item] = "未繳 ❌"
                                                s_df.loc[s_df["座號"] == seat_num, item] = ni
                                                sheets_data[sheet] = s_df
                                    with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
                                        for sheet, s_df in sheets_data.items(): s_df.to_excel(w, sheet_name=sheet, index=False)
                                except: pass
                                st.rerun()
                    
                    st.write("✍️ **隨手備註：**")
                    current_memo = "" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])
                    nm = st.text_input(f"備註_{seat_num}", value=current_memo, placeholder="輸入日常備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}")
                    if nm != current_memo:
                        df.loc[df["座號"] == seat_num, "備註事項"] = nm
                        save_data(df, date_str)

st.markdown("---")
st.markdown(f"<h3 style='color:#FFFFFF;'>📊 801班 {date_str} 綜合班務總表（唯讀檢視）</h3>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
