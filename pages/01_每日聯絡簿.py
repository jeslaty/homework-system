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

    # 嘗試讀取 Excel，若損毀則自動刪除重建
    try:
        with pd.ExcelFile(FILE_NAME, engine="openpyxl") as xl:
            if target_date in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=target_date)
                df["備註事項"] = df["備註事項"].fillna("")
                return df
            else:
                return df_def.copy()
    except Exception:
        # 檔案損毀時刪除舊檔重建，避免持續卡死
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
            df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def

def save_daily_data(updated_df, target_date):
    sheets_data = {}
    # 嘗試讀取原有 Sheet
    if os.path.exists(FILE_NAME):
        try:
            with pd.ExcelFile(FILE_NAME, engine="openpyxl") as xl:
                for sheet in xl.sheet_names:
                    if sheet != target_date:
                        sheets_data[sheet] = pd.read_excel(xl, sheet_name=sheet)
        except Exception:
            # 若舊檔已損毀，直接重置
            sheets_data = {}

    sheets_data[target_date] = updated_df

    # 重新覆寫安全的檔案
    try:
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
            for sheet, s_df in sheets_data.items():
                s_df.to_excel(w, sheet_name=sheet, index=False)
    except Exception as e:
        st.error(f"寫入 Excel 失敗: {e}")
