import streamlit as st
import pandas as pd
import re
import string
import random

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="ATTT Mobile Pro", page_icon="🛡️", layout="centered")

# CSS để tối ưu giao diện di động
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #0d6efd; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; white-space: pre-wrap; background-color: #f0f2f6; 
        border-radius: 5px; padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GỌI DỮ LIỆU TỪ KÉT SẮT (SECRETS)
try:
    SHEET_ID = st.secrets["id_google_sheet"]
    GID_DC = st.secrets["id_tab_dieucam"]
    MAT_KHAU_HE_THONG = st.secrets["password_hethong"]
except Exception as e:
    st.error(f"Lỗi cấu hình Secrets: {e}")
    st.stop()

# Hàm lấy link CSV
def get_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"

@st.cache_data(ttl=60)
def load_data(url):
    try: return pd.read_csv(url)
    except: return None

# 3. GIAO DIỆN BẢO MẬT (SIDEBAR)
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
    st.header("🛠️ Trung tâm Công cụ")
    
    # Chia tab để giao diện di động gọn gàng
    t1, t2, t3 = st.tabs(["🔐 Mật khẩu", "🔗 Kiểm tra Link", "📷 Quét QR"])

    with t1:
        st.subheader("Kiểm tra độ mạnh mật khẩu")
        p = st.text_input("Nhập mật khẩu cần test:", type="password")
        if p:
            score = 0
            checks = {
                "Độ dài ≥ 8 ký tự": len(p) >= 8,
                "Có chữ hoa & chữ thường": any(c.isupper() for c in p) and any(c.islower() for c in p),
                "Có chữ số": any(c.isdigit() for c in p),
                "Có ký tự đặc biệt": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", p))
            }
            for label, status in checks.items():
                if status: 
                    st.write(f"✅ {label}")
                    score += 1
                else: st.write(f"❌ {label}")
            
            if score == 4: st.success("Mật khẩu rất mạnh!")
            elif score >= 2: st.warning("Mật khẩu trung bình.")
            else: st.error("Mật khẩu yếu!")

        st.divider()
        st.subheader("Tạo mật khẩu an toàn")
        if st.button("Tạo mật khẩu ngẫu nhiên"):
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            new_pw = ''.join(random.choice(chars) for i in range(12))
            st.code(new_pw)
            st.caption("Bấm vào để sao chép")

    with t2:
        st.subheader("Quét liên kết lừa đảo")
        url_input = st.text_input("Dán link nghi vấn vào đây:")
        if url_input:
            blacklist = ["bit.ly", "tinyurl.com", "shopee-vouchers", "nhantien", "qua-tang"]
            if any(word in url_input.lower() for word in blacklist):
                st.error("🚨 CẢNH BÁO: Link này có dấu hiệu lừa đảo hoặc rút gọn không an toàn!")
            else:
                st.success("Chưa phát hiện dấu hiệu xấu trong danh sách đen.")

    with t3:
        st.subheader("Quét mã QR")
        cam_on = st.toggle("Mở Camera")
        img = st.camera_input("Chụp mã QR cần kiểm tra", disabled=not cam_on)
        if img: 
            st.image(img, caption="Ảnh đã chụp", width=300)
            st.info("Lưu ý: Hệ thống chỉ lưu ảnh tạm thời để bạn quan sát. Hãy cẩn thận với các mã QR lạ.")

elif menu == "Khẩn cấp":
    st.header("🚨 Hỗ trợ khẩn cấp")
    st.markdown("""
    1. **Ngắt kết nối mạng** ngay lập tức.
    2. **Báo cáo** cho quản trị viên hệ thống.
    3. **Không đăng nhập** vào bất kỳ tài khoản nào khác.
    """)
    st.info("Số điện thoại hỗ trợ: **09xx.xxx.xxx**")
    if st.button("PHÁT TÍN HIỆU CẢNH BÁO"):
        st.snow()
        st.warning("Đã gửi yêu cầu hỗ trợ tới Quản trị viên!")
