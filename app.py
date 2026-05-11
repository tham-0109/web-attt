import streamlit as st
import pandas as pd
import re

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Hệ thống ATTT Mobile", page_icon="🛡️", layout="centered")

# CSS tùy chỉnh để các nút bấm và ô nhập liệu to, dễ bấm trên điện thoại
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #0d6efd; color: white; }
    .stExpander { border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CẤU HÌNH KẾT NỐI GOOGLE SHEETS ---
# Thay 'ID_FILE_CUA_BAN' bằng ID thực tế từ đường link Google Sheets của bạn
GOOGLE_SHEET_ID = "1ppqrGTWXqRDNx2FVxNnMaPrLVan39hrb_9hXJ7oJ98M"

def get_sheet_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid={gid}"

# GID là ID của từng Tab (thường Tab đầu tiên là 0, Tab thứ hai bạn xem ở cuối link web khi bấm vào Tab đó)
URL_TIN_TUC = get_sheet_url("0") 
URL_DIEU_CAM = get_sheet_url("1866776495") # Thay ID Tab Điều Cấm vào đây (ví dụ: 12345678)

@st.cache_data(ttl=60) # Tự động làm mới dữ liệu sau mỗi 60 giây
def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return None

# --- HÀNH LANG BẢO MẬT ---
# Thay vì viết ID và Mật khẩu trực tiếp, hãy dùng dòng này:
GOOGLE_SHEET_ID = st.secrets["1ppqrGTWXqRDNx2FVxNnMaPrLVan39hrb_9hXJ7oJ98M"]
GID_DIEUCAM = st.secrets["1866776495"]
XAC_THUC = st.secrets["123456"]

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=60)
    st.title("Hệ thống Nội bộ")
    pw = st.text_input("Mật khẩu truy cập:", type="password")
    if pw != XAC_THUC:
        st.warning("Vui lòng nhập đúng mật khẩu.")
        st.stop()
    
    st.success("Đã mở khóa")
    menu = st.radio(
        "DANH MỤC",
        ("📰 Tin tức mới", "🚫 Các điều cấm", "🛠️ Công cụ Check", "🚨 Khẩn cấp")
    )

# --- XỬ LÝ NỘI DUNG ---

if menu == "📰 Tin tức mới":
    st.title("📰 Bản tin An toàn thông tin")
    df_news = load_data(URL_TIN_TUC)
    if df_news is not None:
        for _, row in df_news.iterrows():
            with st.expander(f"📌 {row['Ngày']} - {row['Tiêu đề']}"):
                st.write(row['Nội dung'])
    else:
        st.error("Lỗi kết nối dữ liệu Tin tức.")

elif menu == "🚫 Các điều cấm":
    st.title("🚫 Các hành vi bị nghiêm cấm")
    st.info("Danh sách các hành vi vi phạm pháp luật và quy định an toàn mạng.")
    df_prohibited = load_data(URL_DIEU_CAM)
    if df_prohibited is not None:
        for _, row in df_prohibited.iterrows():
            with st.expander(f"❌ {row['Danh mục']}", expanded=True):
                st.write(row['Chi tiết'])
    else:
        st.error("Lỗi kết nối dữ liệu Điều cấm.")

elif menu == "🛠️ Công cụ Check":
    st.title("🛠️ Công cụ kiểm tra nhanh")
    
    # Kiểm tra mật khẩu
    st.subheader("1. Độ mạnh mật khẩu")
    test_pw = st.text_input("Nhập mật khẩu:", type="password")
    if test_pw:
        if len(test_pw) < 8:
            st.error("Quá yếu: Cần ít nhất 8 ký tự.")
        elif not re.search("[0-9]", test_pw) or not re.search("[A-Z]", test_pw):
            st.warning("Trung bình: Nên thêm số và chữ hoa.")
        else:
            st.success("Mật khẩu rất mạnh!")

    # Kiểm tra Link
    st.subheader("2. Quét Link nghi vấn")
    url_in = st.text_input("Dán đường link cần kiểm tra:")
    if url_in:
        bad_words = ['bit.ly', 'tinyurl.com', 'shopee-vouchers', 'larksuite']
        if any(word in url_in.lower() for word in bad_words):
            st.error("🚨 Cảnh báo: Link có dấu hiệu lừa đảo!")
        else:
            st.info("Chưa phát hiện dấu hiệu xấu. Hãy luôn cẩn thận.")

elif menu == "🚨 Khẩn cấp":
    st.title("🚨 Quy trình khẩn cấp")
    st.markdown("""
    ### Khi nghi ngờ bị hack:
    1. **Ngắt mạng** (Tắt Wifi/4G).
    2. **Đăng xuất** tất cả thiết bị từ xa.
    3. **Thay đổi mật khẩu** email khôi phục.
    4. **Liên hệ** phòng kỹ thuật: **0123.456.789**
    """)
    if st.button("GỌI HỖ TRỢ NGAY"):
        st.balloons()
        st.write("Đang kết nối với tổng đài viên...")
