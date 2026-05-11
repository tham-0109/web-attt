import streamlit as st
import pandas as pd
import re
import feedparser

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hệ thống ATTT Mobile", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #0d6efd; color: white; }
    .stExpander { border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀNH LANG BẢO MẬT (Lấy từ Secrets) ---
try:
    ID_SHEET = st.secrets["id_google_sheet"]
    GID_DC = st.secrets["id_tab_dieucam"]
    XAC_THUC = st.secrets["password_hethong"]
except KeyError as e:
    st.error(f"Thiếu cấu hình trong Secrets: {e}")
    st.stop()

# Hàm tạo link chuẩn
def get_sheet_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid={gid}"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return None

# --- 3. SIDEBAR MENU ---
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

# --- 4. XỬ LÝ NỘI DUNG ---

if menu == "📰 Tin tức mới":
    st.title("📰 Bản tin An toàn thông tin")
    
    # Tạo tab để phân loại nguồn tin
    tab_manual, tab_auto = st.tabs(["📌 Tin nội bộ", "🌐 Tin quốc tế"])
    
    with tab_manual:
        st.subheader("Thông báo từ quản trị")
        # Sửa lỗi gọi hàm get_sheet_url ở đây
        df_news = load_data(get_sheet_url("0")) 
        if df_news is not None:
            for _, row in df_news.iterrows():
                with st.expander(f"📍 {row['Ngày']} - {row['Tiêu đề']}"):
                    st.write(row['Nội dung'])
        else:
            st.info("Chưa có tin nội bộ mới.")

    with tab_auto:
        st.subheader("Tin an ninh mạng thế giới")
        rss_url = "https://vnexpress.net/rss/so-hoa/bao-mat.rss"
        feed = feedparser.parse(rss_url)
        if feed.entries:
            for entry in feed.entries[:5]:
                with st.container():
                    st.markdown(f"**[{entry.title}]({entry.link})**")
                    st.caption(f"📅 {entry.published}")
                    st.divider()
        else:
            st.warning("Không thể kết nối lấy tin tự động.")

elif menu == "🚫 Các điều cấm":
    st.title("🚫 Các hành vi bị nghiêm cấm")
    df_prohibited = load_data(get_sheet_url(GID_DC))
    if df_prohibited is not None:
        for _, row in df_prohibited.iterrows():
            with st.expander(f"❌ {row['Danh mục']}", expanded=True):
                st.write(row['Chi tiết'])
    else:
        st.error("Không thể kết nối dữ liệu Điều cấm.")

elif menu == "🛠️ Công cụ Check":
    st.title("🛠️ Công cụ kiểm tra nhanh")
    st.subheader("1. Độ mạnh mật khẩu")
    test_pw = st.text_input("Nhập mật khẩu:", type="password")
    if test_pw:
        if len(test_pw) < 8: st.error("Quá yếu!")
        elif not re.search("[0-9]", test_pw) or not re.search("[A-Z]", test_pw): st.warning("Trung bình.")
        else: st.success("Rất mạnh!")

    st.subheader("2. Quét Link nghi vấn")
    url_in = st.text_input("Dán link:")
    if url_in:
        bad_words = ['bit.ly', 'tinyurl.com', 'shopee', 'lark']
        if any(word in url_in.lower() for word in bad_words): st.error("🚨 Cảnh báo lừa đảo!")
        else: st.info("Chưa thấy dấu hiệu xấu.")

elif menu == "🚨 Khẩn cấp":
    st.title("🚨 Quy trình khẩn cấp")
    st.warning("Hãy ngắt kết nối mạng ngay nếu nghi ngờ bị hack!")
    st.write("- Liên hệ kỹ thuật: **0123.456.789**")
    if st.button("GỌI HỖ TRỢ"):
        st.balloons()
