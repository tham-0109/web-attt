import streamlit as st
import pandas as pd
import re
import string
import random
import feedparser
from PIL import Image

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Sổ tay ATTT", page_icon="🛡️", layout="centered")

# CSS tối ưu di động
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #0d6efd; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. KẾT NỐI DỮ LIỆU (SECRETS)
try:
    ID_SHEET = st.secrets["id_google_sheet"]
    GID_DC = st.secrets["id_tab_dieucam"]
    GID_NC = st.secrets["id_tab_Nguyco"]
    XAC_THUC = st.secrets["password_hethong"]
except Exception as e:
    st.error(f"Lỗi cấu hình Secrets: {e}")
    st.stop()

def get_sheet_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid={gid}"

@st.cache_data(ttl=60)
def load_data(url):
    try: return pd.read_csv(url)
    except: return None

#3. GIAO DIỆN BẢO MẬT (SIDEBAR)
with st.sidebar:
    st.title("🛡️ SỔ TAY ATTT")
    pw = st.text_input("Mật khẩu truy cập:", type="password")
    
    # Nếu mật khẩu sai hoặc chưa nhập
    if pw != XAC_THUC:
        st.warning("Vui lòng nhập mật khẩu chính xác để mở khóa tài liệu.")
        # Dừng xử lý các menu bên dưới
        menu = None 
    else:
        st.success("Đã mở khóa hệ thống")
        menu = st.radio("DANH MỤC", (
            "📰 Tin tức", 
            "🚫 Các điều cấm", 
            "🛡️ Nguy cơ & Biện pháp", 
            "🛠️ Công cụ", 
            "🚨 Khẩn cấp"
        ))

# 4. XỬ LÝ NỘI DUNG CHÍNH
if pw != password_hethong:
    # 1. CĂN GIỮA LOGO BẰNG COLUMNS
    st.markdown("<br><br>", unsafe_allow_html=True) # Tạo khoảng trống trên cùng
    col1, col2, col3 = st.columns([1, 2, 1]) # Chia màn hình thành 3 phần, phần giữa rộng gấp đôi
    
    with col2:
        # Thay link logo Khiên bảo mật vào đây và căn giữa ảnh
        st.image("https://cdn-icons-png.flaticon.com/512/1067/1067357.png", width=150)
    
    # 2. CĂN GIỮA CHỮ BẰNG HTML CSS
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>SỔ TAY ATTT MOBILE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Hệ thống tra cứu quy định và tin tức bảo mật nội bộ</p>", unsafe_allow_html=True)
    
    st.divider()
    st.info("👈 **HƯỚNG DẪN:** Vui lòng nhập mật khẩu ở thanh Menu bên trái (hoặc nhấn vào dấu mũi tên góc trên cùng bên trái trên điện thoại) để xem nội dung.")
    st.caption("<p style='text-align: center;'>Bản quyền © 2026 - Đội ngũ ATTT</p>", unsafe_allow_html=True)

# Nếu đã có mật khẩu thì mới hiện các nội dung menu
elif menu == "📰 Tin tức":
    # (Giữ nguyên đoạn code tin tức cũ của bạn tại đây)
    st.header("📰 Bản tin An toàn thông tin")

if menu == "📰 Tin tức":
    st.header("📰 Bản tin An toàn thông tin")
    t1, t2 = st.tabs(["📌 Tin nội bộ", "🌐 Tin quốc tế"])
    with t1:
        df = load_data(get_sheet_url("0"))
        if df is not None:
            for _, row in df.iterrows():
                with st.expander(f"📍 {row['Ngày']} - {row['Tiêu đề']}"):
                    st.write(row['Nội dung'])
    with t2:
        feed = feedparser.parse("https://vnexpress.net/rss/so-hoa/bao-mat.rss")
        if feed.entries:
            for entry in feed.entries[:5]:
                st.markdown(f"**[{entry.title}]({entry.link})**")
                st.caption(f"📅 {entry.published}")
                st.divider()

elif menu == "🚫 Các điều cấm":
    st.header("🚫 Quy định nghiêm cấm")
    df_dc = load_data(get_sheet_url(GID_DC))
    if df_dc is not None:
        for _, row in df_dc.iterrows():
            st.error(f"❌ {row['Danh mục']}")
            st.write(row['Chi tiết'])
            st.divider()

elif menu == "🛡️ Nguy cơ & Biện pháp":
    st.header("🛡️ Nhận diện Nguy cơ & Phòng ngừa")
    df_risk = load_data(get_sheet_url(GID_NC))
    if df_risk is not None:
        for _, row in df_risk.iterrows():
            with st.expander(f"⚠️ {row['Nguy cơ']}"):
                st.info(f"**Biện pháp bảo đảm:**\n\n{row['Biện pháp bảo đảm']}")
    else:
        st.error("Chưa thể kết nối dữ liệu Nguy cơ.")

elif menu == "🛠️ Công cụ":
    st.header("🛠️ Trung tâm Công cụ")
    tab_pw, tab_link, tab_qr = st.tabs(["🔐 Mật khẩu", "🔗 Kiểm tra Link", "📷 Quét QR"])
    with tab_pw:
        p = st.text_input("Kiểm tra mật khẩu:", type="password")
        if p:
            score = sum([len(p)>=8, any(c.isupper() for c in p), any(c.isdigit() for c in p)])
            if score == 3: st.success("Mật khẩu mạnh")
            else: st.warning("Mật khẩu cần cải thiện")
    with tab_qr:
        from pyzbar.pyzbar import decode
        img = st.camera_input("Quét mã QR")
        if img:
            res = decode(Image.open(img))
            if res:
                content = res[0].data.decode("utf-8")
                st.success("Nội dung mã QR:")
                st.code(content)
            else: st.warning("Không tìm thấy mã.")

elif menu == "🚨 Khẩn cấp":
    st.header("🚨 Phản ứng Sự cố")
    st.warning("⚡ HÀNH ĐỘNG NGAY:")
    st.checkbox("1. Ngắt kết nối Internet thiết bị.")
    st.checkbox("2. Thông báo ngay cho quản trị viên kỹ thuật.")
    # Sửa lỗi Syntax tại đây bằng cách bọc markdown chuẩn
    st.markdown("[📞 GỌI HOTLINE HỖ TRỢ](tel:0378765992)", unsafe_allow_html=True)
