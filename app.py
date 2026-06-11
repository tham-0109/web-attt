import streamlit as st
import pandas as pd
import feedparser
from pyzbar.pyzbar import decode
from PIL import Image
import secrets
import string
import time


st.set_page_config(
    page_title="Sổ tay ATTT",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'login_attempts' not in st.session_state:
    st.session_state['login_attempts'] = 0
if 'last_activity' not in st.session_state:
    st.session_state['last_activity'] = time.time()
if 'locked_until' not in st.session_state:
    st.session_state['locked_until'] = 0

# Session timeout (15 minutes = 900 seconds)
SESSION_TIMEOUT = 900

# Check session timeout
if st.session_state['authenticated']:
    current_time = time.time()
    if current_time - st.session_state['last_activity'] > SESSION_TIMEOUT:
        st.session_state['authenticated'] = False
        st.warning("Phiên làm việc đã hết hạn. Vui lòng đăng nhập lại.")
        st.rerun()
    else:
        st.session_state['last_activity'] = current_time

try:
    ID_SHEET = st.secrets["id_google_sheet"]
    GID_DC = st.secrets["id_tab_dieucam"]
    GID_NC = st.secrets["id_tab_nguyco"]
    MAT_KHAU_HE_THONG = st.secrets["password_hethong"]
except Exception as e:
    st.error("Vui lòng cấu hình các secrets trong Streamlit!")
    st.stop()


def get_sheet_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid={gid}"


@st.cache_data(ttl=60)
def load_data(url):
    return pd.read_csv(url)


st.sidebar.title("🔐 Xác thực")

# Check if account is locked
current_time = time.time()
if st.session_state['locked_until'] > current_time:
    remaining = int(st.session_state['locked_until'] - current_time)
    st.sidebar.error(f"Tài khoản bị khóa. Thử lại sau {remaining} giây.")
else:
    password = st.sidebar.text_input("Nhập mật khẩu", type="password", key="password_input")
    
    if password:
        if password == MAT_KHAU_HE_THONG:
            st.session_state['authenticated'] = True
            st.session_state['login_attempts'] = 0
            st.session_state['last_activity'] = time.time()
            st.sidebar.success("Xác thực thành công!")
        else:
            st.session_state['login_attempts'] += 1
            if st.session_state['login_attempts'] >= 5:
                st.session_state['locked_until'] = time.time() + 120
                st.sidebar.error("Quá nhiều lần thử sai. Tài khoản bị khóa 2 phút!")
            else:
                st.sidebar.error(f"Mật khẩu không đúng! Còn {5 - st.session_state['login_attempts']} lần thử.")

menu = None
if st.session_state['authenticated']:
    menu = st.sidebar.radio(
        "Danh mục",
        ["📰 Tin tức", "🚫 Các điều cấm", "🛡️ Nguy cơ & Biện pháp", "🛠️ Công cụ", "🚨 Khẩn cấp"]
    )
    if st.sidebar.button("🚪 Đăng xuất"):
        st.session_state['authenticated'] = False
        st.rerun()

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1067/1067357.png", width=150)
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>SỔ TAY ATTT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Hệ thống tra cứu an toàn thông tin nội bộ</p>", unsafe_allow_html=True)
    st.info("👈 HƯỚNG DẪN: Nhấn vào dấu Menu hoặc mũi tên ở góc trái bên trên điện thoại và nhập mật khẩu để bắt đầu.")

else:
    if menu == "📰 Tin tức":
        tab1, tab2 = st.tabs(["📌 Tin nội bộ", "🌐 Tin quốc tế"])
        with tab1:
            st.header("📌 Tin nội bộ")
            with st.spinner("Đang tải dữ liệu..."):
                try:
                    df_tin_noi_bo = load_data(get_sheet_url("0"))
                    for i, row in df_tin_noi_bo.iterrows():
                        with st.expander(f"📄 {row.iloc[0] if len(row) > 0 else 'Tiêu đề'}"):
                            st.write(row.iloc[1] if len(row) > 1 else "Nội dung")
                except Exception as e:
                    st.warning("Chưa cấu hình Google Sheets hoặc không thể kết nối.")
        with tab2:
            st.header("🌐 Tin quốc tế")
            with st.spinner("Đang tải dữ liệu..."):
                try:
                    feed = feedparser.parse("https://vnexpress.net/rss/so-hoa/bao-mat.rss")
                    for entry in feed.entries[:5]:
                        st.markdown(f"**[{entry.title}]({entry.link})**")
                        st.write(entry.summary)
                        st.divider()
                except Exception as e:
                    st.error("Không thể tải RSS feed.")

    elif menu == "🚫 Các điều cấm":
        st.header("🚫 Các điều cấm")
        with st.spinner("Đang tải dữ liệu..."):
            try:
                df_dieu_cam = load_data(get_sheet_url(GID_DC))
                for i, row in df_dieu_cam.iterrows():
                    st.error(f"❌ {row.iloc[0] if len(row) > 0 else 'Điều cấm'}")
                    st.write(row.iloc[1] if len(row) > 1 else "Chi tiết")
            except Exception as e:
                st.warning("Không thể tải dữ liệu điều cấm.")

    elif menu == "🛡️ Nguy cơ & Biện pháp":
        st.header("🛡️ Nguy cơ & Biện pháp")
        with st.spinner("Đang tải dữ liệu..."):
            try:
                df_nguy_co = load_data(get_sheet_url(GID_NC))
                icons = ["⚠️", "🔓", "📧", "🔗", "💻"]
                for i, row in df_nguy_co.iterrows():
                    icon = icons[i % len(icons)]
                    with st.expander(f"{icon} {row.iloc[0] if len(row) > 0 else 'Nguy cơ'}"):
                        st.info(f"✅ Biện pháp: {row.iloc[1] if len(row) > 1 else 'Biện pháp bảo vệ'}")
            except Exception as e:
                st.warning("Không thể tải dữ liệu nguy cơ.")

    elif menu == "🛠️ Công cụ":
        tab1, tab2, tab3 = st.tabs(["🔐 Mật khẩu", "🔗 Kiểm tra Link", "📷 Quét mã QR"])
        with tab1:
            st.header("🔐 Kiểm tra và tạo mật khẩu")
            input_pass = st.text_input("Nhập mật khẩu để kiểm tra", type="password")
            if input_pass:
                score = 0
                has_upper = any(c.isupper() for c in input_pass)
                has_lower = any(c.islower() for c in input_pass)
                has_digit = any(c.isdigit() for c in input_pass)
                has_special = any(c in "!@#$%^&*" for c in input_pass)
                
                if len(input_pass) >= 8: score +=1
                if has_upper: score +=1
                if has_lower: score +=1
                if has_digit: score +=1
                if has_special: score +=1
                
                if score == 5:
                    st.success("✅ Mật khẩu rất mạnh!")
                elif score >= 3:
                    st.warning("⚠️ Mật khẩu trung bình")
                else:
                    st.error("❌ Mật khẩu yếu!")
            if st.button("🎲 Tạo mật khẩu ngẫu nhiên"):
                chars = string.ascii_letters + string.digits + "!@#$%^&*"
                random_pass = ''.join(secrets.choice(chars) for _ in range(16))
                st.code(random_pass)
        with tab2:
            st.header("🔗 Kiểm tra Link")
            link = st.text_input("Dán link cần kiểm tra")
            if link:
                keywords = ["bit.ly", "tinyurl", "shopee", "larksuite", "bom.so"]
                if any(kw in link.lower() for kw in keywords):
                    st.error("❌ CẢNH BÁO: Link có khả năng lừa đảo!")
                elif not link.startswith("https://"):
                    st.warning("⚠️ CẢNH BÁO: Link không dùng HTTPS (không bảo mật)")
                else:
                    st.success("✅ Link an toàn (dùng HTTPS)")
        with tab3:
            st.header("📷 Quét mã QR")
            enable_camera = st.toggle("Bật camera")
            if enable_camera:
                img_file = st.camera_input("Chụp mã QR")
                if img_file:
                    img = Image.open(img_file)
                    decoded = decode(img)
                    if decoded:
                        st.code(decoded[0].data.decode('utf-8'))
                    else:
                        st.warning("Không tìm thấy mã QR trong ảnh.")

    elif menu == "🚨 Khẩn cấp":
        st.header("🚨 Quy trình phản ứng khẩn cấp")
        st.markdown("### 📋 Checklist hành động:")
        
        # Initialize checklist states in session_state
        if 'checklist' not in st.session_state:
            st.session_state['checklist'] = {
                'ngat_internet': False,
                'thong_bao': False,
                'khong_tat_may': False,
                'ghi_lai': False
            }
        
        st.session_state['checklist']['ngat_internet'] = st.checkbox(
            "❌ Ngắt kết nối internet/Wi-Fi ngay lập tức",
            value=st.session_state['checklist']['ngat_internet']
        )
        st.session_state['checklist']['thong_bao'] = st.checkbox(
            "📞 Thông báo quản trị viên an toàn thông tin",
            value=st.session_state['checklist']['thong_bao']
        )
        st.session_state['checklist']['khong_tat_may'] = st.checkbox(
            "💾 Không tắt máy, giữ nguyên hiện trạng để điều tra",
            value=st.session_state['checklist']['khong_tat_may']
        )
        st.session_state['checklist']['ghi_lai'] = st.checkbox(
            "📝 Ghi lại mọi chi tiết nghi ngờ",
            value=st.session_state['checklist']['ghi_lai']
        )
        
        st.divider()
        st.markdown("[📞 GỌI HOTLINE HỖ TRỢ](tel:0901234567)")
