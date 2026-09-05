import os
import pandas as pd
import streamlit as st

# 設定網頁標題與圖示
st.set_page_config(page_title="國中學生作業管理系統", page_icon="🍎", layout="wide")

# 🎨 注入馬卡龍粉紅、粉藍與樣式美化
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F2 !important; }
    [data-testid="stSidebar"] { background-color: #E6F2FF !important; }
    h1, h2, h3 { color: #4A4A4A !important; font-family: "Helvetica Neue", Arial, "Noto Sans TC", sans-serif; }
    .stText, p, span, label { color: #333333 !important; }
    </style>
""", unsafe_allow_html=True)

# 🔑 帳號密碼設定（老師您可以在這裡修改成您想要的帳密）
USER_USERNAME = "Tseng"
USER_PASSWORD = "12345"

# 初始化登入狀態
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ----------------- 登入畫面 -----------------
if not st.session_state["logged_in"]:
    st.title("🔒 歡迎使用作業管理系統")
    st.write("請輸入教師帳號與密碼以開始使用。")
    
    # 建立一個乾淨的登入區塊
    with st.form("login_form"):
        input_username = st.text_input("教師帳號：")
        input_password = st.text_input("登入密碼：", type="password")
        submit_button = st.form_submit_button("確認登入")
        
        if submit_button:
            if input_username == USER_USERNAME and input_password == USER_PASSWORD:
                st.session_state["logged_in"] = True
                st.success("🎉 登入成功！")
                st.rerun()
            else:
                st.error("❌ 帳號或密碼錯誤，請重新輸入。")
    st.stop() # 沒登入成功的話，程式就停在這裡，不顯示後面的名單

# ----------------- 系統主畫面 (登入後才會顯示) -----------------
st.title("🍎 國中學生作業管理系統")

# 提供登出按鈕在左側最上方
if st.sidebar.button("🔒 安全登出"):
    st.session_state["logged_in"] = False
    st.rerun()

# 純文字符號串接名單
seats_801_str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28"
seats_903_str = "1,2,3,4,5,6,7,8,9,10,11,12,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29"
seats_904_str = "1,2,3,4,5,6,7,8,9,10,11,12,15,16,17,18,19,20,21,22,23,24,25,26,27"
seats_906_str = "1,3,4,5,6,7,8,9,10,11,12,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,31,32"

# 【內建全班學生名單資料庫】
STUDENT_DATABASE = {
    "801班": {
        "座號": [int(x) for x in seats_801_str.split(",")],
        "姓名": ["王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", "黃榆涵", "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", "董子以", "劉家佑", "魏辰恩"]
    },
    "903班": {
        "座號": [int(x) for x in seats_903_str.split(",")],
        "姓名": ["張莘妍", "梁芯瑜", "吳佳錹", "許秧秧", "陳又綺", "高筱媗", "莊子玉", "吳愷昕", "陳以恩", "蕭妤柔", "吳璥齡", "魏品儀", "邱子恆", "張本維", "謝易宸", "游子宥", "吳宇曜", "吳嘉恩", "丁沛紳", "林子佑", "陳冠成", "徐國睿", "余冠憲", "黃家寶", "張瑋志", "方仲祺", "林昱嘉"]
    },
    "904班": {
        "座號": [int(x) for x in seats_904_str.split(",")],
        "姓名": ["戴嘉妤", "陳資晴", "傅詩穎", "張瞳恩", "黃宇婕", "吳沛媛", "李妍芯", "鄭羽恩", "林子桐", "許詠晴", "吳宸彤", "林品妍", "趙右群", "林定毅", "潘子堯", "郭羿楷", "張明哲", "吳宇曜", "魏永聖", "游承恩", "胡琮浩", "李柏沅", "許育政", "宗旻恩", "吳博硯"]
    },
    "906班": {
        "座號": [int(x) for x in seats_906_str.split(",")],
        "姓名": ["陳亮妤", "董宜洳", "林庭瑜", "許淯淳", "陳鈺軒", "林郁庭", "陳雅竹", "陳睿瑤", "楊淇暄", "陳雨萱", "江霈穎", "陳逸恩", "劉哲皓", "陳士愷", "李開哲", "林翊凱", "林晉宇", "林釉荏", "林均昊", "賴羿軒", "鄧仲喆", "吳羽翔", "林擎宇", "林旻勳", "鄭凱軒", "李秉叡", "曾群文", "吳立丞"]
    }
}

# 1. 班級選擇（左側邊欄）
st.sidebar.header("🏫 班級管理")
class_list = list(STUDENT_DATABASE.keys())
selected_class = st.sidebar.selectbox("請選擇班級：", class_list)

FILE_NAME = f"學生作業紀錄_{selected_class}.xlsx"

# 2. 初始化該班級的 Excel 檔案
def load_data():
    if not os.path.exists(FILE_NAME):
        default_data = {
            "座號": STUDENT_DATABASE[selected_class]["座號"],
            "姓名": STUDENT_DATABASE[selected_class]["姓名"],
        }
        df = pd.DataFrame(default_data)
        df.to_excel(FILE_NAME, index=False)
    return pd.read_excel(FILE_NAME)

df = load_data()

# 3. 功能區：新增作業
st.sidebar.markdown("---")
st.sidebar.subheader("➕ 新增作業項目")
new_assignment = st.sidebar.text_input("輸入新作業名稱：", placeholder="例如：數學習作 P.10")
if st.sidebar.button("建立作業欄位"):
    if new_assignment:
        if new_assignment in df.columns:
            st.sidebar.error("⚠️ 該作業名稱已存在！")
        else:
            df[new_assignment] = "未繳"
            df.to_excel(FILE_NAME, index=False)
            st.sidebar.success(f"✅ 已成功新增：{new_assignment}")
            st.rerun()
    else:
        st.sidebar.warning("⚠️ 請輸入作業名稱")

# 檢查是否有作業欄位
has_assignments = len(df.columns) > 2

# 4. 主畫面：選擇要登記或查看的作業
if has_assignments:
    assignment_list = list(df.columns[2:])
    current_assign = st.selectbox("🎯 請選擇要登記/查看的作業：", assignment_list)

    col1, col_space, col2 = st.columns([5, 1, 4])

    with col1:
        st.subheader(f"📝 {selected_class} - 狀態點選登記")
        st.caption("點選後系統會即時自動存檔")
        st.write("") 

        for index, row in df.iterrows():
            seat = int(row["座號"])
            name = row["姓名"]
            current_status = row[current_assign]

            options = ["未繳", "已繳", "缺交"]
            try:
                default_idx = options.index(current_status)
            except ValueError:
                default_idx = 0

            c_seat, c_name, c_radio = st.columns([1, 2, 4])
            c_seat.write(f"**{seat} 號**")
            c_name.write(name)

            new_status = c_radio.radio(
                f"狀態_{seat}",
                options,
                index=default_idx,
                horizontal=True,
                label_visibility="collapsed",
                key=f"radio_{seat}_{current_assign}",
            )

            if new_status != current_status:
                df.loc[df["座號"] == seat, current_assign] = new_status
                df.to_excel(FILE_NAME, index=False)
                st.rerun()

    with col2:
        st.subheader("📋 催繳名單與統計")
        st.write("") 

        total_students = len(df)
        paid_count = len(df[df[current_assign] == "已繳"])
        st.metric(label="繳交進度", value=f"{paid_count} / {total_students} 人")

        missing_df = df[df[current_assign].isin(["未繳", "缺交"])]

        if missing_df.empty:
            st.balloons()
            st.success("🎉 太棒了！全班皆已繳齊！")
        else:
            st.error(f"❌ 尚未繳交名單 ({len(missing_df)} 人)：")
            missing_text = f"【{selected_class} {current_assign} 未繳名單】\n"
            for _, row in missing_df.iterrows():
                missing_text += f"{int(row['座號'])}號 {row['姓名']} ({row[current_assign]})\n"

            st.text_area("可直接複製文字傳至群組：", value=missing_text, height=250)

    st.markdown("---")
    st.subheader("📊 全班作業總表（唯讀檢視）")
    st.dataframe(df, use_container_width=True)

else:
    st.info("💡 目前還沒有任何作業項目。請先在左側邊欄輸入名稱並點選「建立作業欄位」！")
