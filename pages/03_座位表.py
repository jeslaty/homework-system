import os
import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="03_座位表管理", page_icon="🪑", layout="wide")

# CSS 視覺優化
st.markdown("""
    <style>
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp {
        background-color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    .title-banner {
        background: linear-gradient(135deg, #0284C7 0%, #38BDF8 100%);
        color: white; padding: 18px 24px; border-radius: 16px; margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.15);
    }
    .title-banner h1 { color: #FFFFFF !important; font-size: 1.7rem !important; margin: 0 !important; }
    
    /* 講台樣式 */
    .podium {
        background-color: #475569;
        color: white;
        text-align: center;
        padding: 10px;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 25px;
        letter-spacing: 2px;
    }
    
    /* 座位卡片樣式 */
    .seat-card {
        background-color: #FFFFFF;
        border: 2px solid #BAE6FD;
        border-radius: 14px;
        padding: 12px 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .seat-card:hover {
        border-color: #0284C7;
        transform: translateY(-2px);
    }
    .seat-num {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 600;
    }
    .seat-name {
        font-size: 1.1rem;
        color: #0F172A;
        font-weight: 700;
        margin-top: 4px;
    }
    .seat-empty {
        background-color: #F1F5F9;
        border: 2px dashed #CBD5E1;
        color: #94A3B8;
    }
    </style>
""", unsafe_allow_html=True)

# 801 班學生名單 (28人)
STUDENTS_801 = [
    (1, '王喬昕'), (2, '吳岢曈'), (3, '李巧彤'), (4, '岳昀軒'), (5, '林晏以'),
    (6, '林晨琳'), (7, '林芮妘'), (8, '林苡嫻'), (9, '黃榆涵'), (10, '黃榆涵'),
    (11, '蔡可琳'), (12, '戴彤竹'), (13, '羅羽翎'), (14, '羅昕彤'), (15, '林禹彤'),
    (16, '王楷文'), (17, '王駿展'), (18, '吳軒佑'), (19, '李宇哲'), (20, '林柏辰'),
    (21, '張品御'), (22, '陳正澤'), (23, '陳秉玄'), (24, '陳鼎硯'), (25, '黃楙軒'),
    (26, '董子以'), (27, '劉家佑'), (28, '魏辰恩')
]

SEAT_FILE = "801班_座位表.csv"

# 載入或初始化座位資料
def load_seats():
    if os.path.exists(SEAT_FILE):
        try:
            return pd.read_csv(SEAT_FILE).to_dict('records')
        except:
            pass
    # 預設按座號順序排列
    seats = []
    for s in STUDENTS_801:
        seats.append({"座號": s[0], "姓名": s[1]})
    return seats

def save_seats(seats_data):
    df = pd.DataFrame(seats_data)
    df.to_csv(SEAT_FILE, index=False, encoding="utf-8-sig")

if "seats_801" not in st.session_state:
    st.session_state["seats_801"] = load_seats()

# 頂部控制欄
col_top_title, col_top_back = st.columns([0.80, 0.20])
with col_top_title:
    st.markdown('<div class="title-banner"><h1>🪑 801 班級座位表管理系統</h1></div>', unsafe_allow_html=True)
with col_top_back:
    if st.button("🏛️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")

# 功能操作區
col_ctrl, col_info = st.columns([0.3, 0.7])
with col_ctrl:
    if st.button("🎲 隨機重新抽籤排座位", type="primary", use_container_width=True):
        shuffled = st.session_state["seats_801"].copy()
        random.shuffle(shuffled)
        st.session_state["seats_801"] = shuffled
        save_seats(shuffled)
        st.toast("✅ 已成功重排座位並儲存！", icon="✨")
        st.rerun()

with col_info:
    st.caption("💡 配置說明：全班共 28 人，規劃為 6 排（從教師講台視角看過去：第 1~5 排每排 5 人，第 6 排 3 人）。")

st.markdown("---")

# 模擬講台畫面
st.markdown('<div class="podium">📺 黑板 / 教師講台區（老師視角：左 👈 🪑 👉 右）</div>', unsafe_allow_html=True)

# 依 6 排配置計算座位矩陣 (前 5 排每排 5 人，第 6 排 3 人)
# 座位總空間為 6 列 x 5 行，第 6 排僅填前 3 行
seats_list = st.session_state["seats_801"]
total_seats = len(seats_list)

seat_idx = 0
for row_idx in range(6): # 6 排
    cols = st.columns(5, gap="medium") # 最多 5 直欄
    max_in_row = 5 if row_idx < 5 else 3
    
    for col_idx in range(5):
        with cols[col_idx]:
            if col_idx < max_in_row and seat_idx < total_seats:
                student = seats_list[seat_idx]
                st.markdown(f"""
                    <div class="seat-card">
                        <div class="seat-num">{student['座號']} 號</div>
                        <div class="seat-name">{student['姓名']}</div>
                    </div>
                """, unsafe_allow_html=True)
                seat_idx += 1
            else:
                # 空位（第6排的最後2個位置）
                st.markdown("""
                    <div class="seat-card seat-empty">
                        <div class="seat-num">-</div>
                        <div class="seat-name">走道/空位</div>
                    </div>
                """, unsafe_allow_html=True)
