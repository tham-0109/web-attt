import streamlit as st
import pandas as pd
import re
import feedparser

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Hệ thống ATTT Mobile", page_icon="🛡️", layout="centered")

# SỬA LỖI Ở ĐÂY: Dùng unsafe_allow_html
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #0d6efd; color: white; }
    .stExpander { border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BẢO MẬT & KẾT NỐI (Lấy từ Secrets) ---
try:
    ID_SHEET = st.secrets["id_google_sheet"]
    GID_DC = st.secrets["id_tab_dieucam"]
    XAC_THUC = st.secrets["password_hethong"]
except Exception as e:
    st.error("Lỗi: Chưa cấu hình Secrets trên Streamlit Cloud!")
    st.stop()

def get_sheet_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid={gid}"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception:
        return None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=60)
    st.title("Hệ thống Nội bộ")
    pw = st.text_input("Mật khẩu truy cập:", type="password")
    if pw != XAC_THUC:
        st.warning("Vui lòng nhập đúng mật khẩu.")
        st.stop()
    
    st.success("Đã mở khóa")
    menu = st.radio("DANH MỤC", ("📰 Tin tức mới", "🚫 Các điều cấm", "🛠️ Công cụ Check", "🚨 Khẩn cấp"))

# --- 4. XỬ LÝ NỘI DUNG ---
if menu == "📰 Tin tức mới":
    st.title("📰 Bản tin An toàn thông tin")
    tab_manual, tab_auto = st.tabs(["📌 Tin nội bộ", "🌐 Tin quốc tế"])
    
    with tab_manual:
        df_news = load_data(get_sheet_url("0")) # Tab đầu tiên thường là GID=0
        if df_news is not None:
            for _, row in df_news.iterrows():
                with st.expander(f"📍 {row['Ngày']} - {row['Tiêu đề']}"):
                    st.write(row['Nội dung'])
        else:
            st.error("Không thể kết nối dữ liệu Google Sheets. Hãy kiểm tra quyền chia sẻ file!")

    with tab_auto:
        st.subheader("Tin an ninh mạng thế giới")
        # Sử dụng RSS của VnExpress
        feed = feedparser.parse("https://vnexpress.net/rss/so-hoa/bao-mat.rss")
        if feed.entries:
            for entry in feed.entries[:5]:
                with st.container():
                    st.markdown(f"**[{entry.title}]({entry.link})**")
                    st.caption(f"📅 {entry.published}")
                    st.divider()
        else:
            st.warning("Không thể lấy tin tự động. Kiểm tra file requirements.txt đã có 'feedparser' chưa.")

elif menu == "🚫 Các điều cấm":
    st.title("🚫 Các hành vi bị nghiêm cấm")
    df_prohibited = load_data(get_sheet_url(GID_DC))
    if df_prohibited is not None:
        for _, row in df_prohibited.iterrows():
            with st.expander(f"❌ {row['Danh mục']}", expanded=True):
                st.write(row['Chi tiết'])
    else:
        st.error("Lỗi kết nối dữ liệu Điều cấm.")

elif menu == "🛠️ Công cụ Check":
    st.title("🛠️ Công cụ kiểm tra nhanh")
    st.subheader("1. Độ mạnh mật khẩu")
    test_pw = st.text_input("Nhập mật khẩu:", type="password")
    if test_pw:
        if len(test_pw) < 8: st.error("Quá yếu!")
        else: st.success("Mật khẩu tốt.")

elif menu == "🚨 Khẩn cấp":
    st.title("🚨 Quy trình khẩn cấp")
    st.write("- Liên hệ kỹ thuật: **0123.456.789**")
    if st.button("PHÁT TÍN HIỆU"): st.snow()
