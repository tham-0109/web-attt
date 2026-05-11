import streamlit as st
import pandas as pd
import re

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Hệ thống ATTT Mobile", page_icon="🛡️")

# --- KẾT NỐI DỮ LIỆU GOOGLE SHEETS ---
# THAY LINK DƯỚI ĐÂY BẰNG LINK CỦA BẠN (đã đổi đuôi thành /export?format=csv)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ppqrGTWXqRDNx2FVxNnMaPrLVan39hrb_9hXJ7oJ98M/export?format=csv"

def load_data():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return None

# 2. BẢO MẬT TRUY CẬP
XAC_THUC = "123456" 

with st.sidebar:
    st.title("🛡️ Quản trị")
    pw_input = st.text_input("Mật khẩu:", type="password")
    if pw_input != XAC_THUC:
        st.warning("Vui lòng nhập mật khẩu.")
        st.stop()
    
    menu = st.radio("CHỨC NĂNG", ("📰 Tin tức", "🛠️ Công cụ", "🚨 Khẩn cấp"))

# 3. NỘI DUNG CHÍNH
if menu == "📰 Tin tức":
    st.title("📰 Bản tin An toàn thông tin")
    df = load_data()
    
    if df is not None:
        for index, row in df.iterrows():
            with st.expander(f"📌 {row['Ngày']} - {row['Tiêu đề']}"):
                st.write(row['Nội dung'])
    else:
        st.error("Không thể kết nối với dữ liệu Google Sheets.")

elif menu == "🛠️ Công cụ":
    st.title("🛠️ Công cụ bảo mật")
    # (Giữ lại các code kiểm tra mật khẩu và link từ bước trước ở đây)
    pw = st.text_input("Kiểm tra mật khẩu:", type="password")
    if pw:
        if len(pw) >= 8: st.success("Mật khẩu đủ độ dài.")
        else: st.error("Mật khẩu quá ngắn.")

elif menu == "🚨 Khẩn cấp":
    st.title("🚨 Hướng dẫn xử lý nhanh")
    st.info("Hãy gọi 113 hoặc bộ phận IT nếu bạn nghi ngờ bị tấn công hệ thống.")
