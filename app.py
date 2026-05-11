import streamlit as st
import pandas as pd
import re

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="ATTT Mobile Pro", page_icon="🛡️")

# 2. GỌI DỮ LIỆU TỪ KÉT SẮT (SECRETS)
try:
    SHEET_ID = st.secrets["id_google_sheet"]
    GID_DC = st.secrets["id_tab_dieucam"]
    MAT_KHAU_HE_THONG = st.secrets["password_hethong"]
except:
    st.error("Lỗi: Bạn chưa thiết lập 'Secrets' trên Streamlit Cloud!")
    st.stop()

# Hàm lấy link CSV
def get_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"

@st.cache_data(ttl=60)
def load_data(url):
    try: return pd.read_csv(url)
    except: return None

# 3. GIAO DIỆN BẢO MẬT
with st.sidebar:
    st.title("🛡️ SECURITY SYSTEM")
    pw = st.text_input("Mật khẩu truy cập:", type="password")
    if pw != MAT_KHAU_HE_THONG:
        st.info("Vui lòng nhập mật khẩu để tiếp tục.")
        st.stop()
    
    st.success("Xác thực thành công!")
    menu = st.radio("MENU CHÍNH", ("Bản tin", "Các điều cấm", "Công cụ", "Khẩn cấp"))

# 4. XỬ LÝ CÁC MỤC
if menu == "Bản tin":
    st.header("📰 Tin tức An toàn mạng")
    df = load_data(get_url("0"))
    if df is not None:
        for _, row in df.iterrows():
            with st.expander(f"📌 {row['Ngày']} - {row['Tiêu đề']}"):
                st.write(row['Nội dung'])

elif menu == "Các điều cấm":
    st.header("🚫 Hành vi bị nghiêm cấm")
    df_dc = load_data(get_url(GID_DC))
    if df_dc is not None:
        for _, row in df_dc.iterrows():
            st.error(f"❌ {row['Danh mục']}")
            st.write(row['Chi tiết'])
            st.divider()

elif menu == "Công cụ":
    st.header("🛠️ Công cụ hỗ trợ")
    # Check pass
    st.subheader("Kiểm tra mật khẩu")
    p = st.text_input("Nhập pass:", type="password")
    if p:
        st.write("Độ dài:", len(p))
    
    st.divider()
    # Camera
    st.subheader("📷 Quét mã QR")
    cam_on = st.toggle("Kích hoạt Camera")
    img = st.camera_input("Chụp ảnh", disabled=not cam_on)
    if img: st.image(img, width=250)

elif menu == "Khẩn cấp":
    st.header("🚨 Hỗ trợ khẩn cấp")
    st.write("1. Tắt mạng thiết bị.")
    st.write("2. Liên hệ Admin: 09xx.xxx.xxx")
    if st.button("KÍCH HOẠT CẢNH BÁO"):
        st.snow()
        st.warning("Đã gửi thông báo khẩn cấp cho Quản trị viên!")
