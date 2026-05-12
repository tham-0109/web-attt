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
if pw != XAC_THUC:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Căn giữa logo bằng cột
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", use_container_width=True)
    
    st.markdown("<h1 class='main-title'>SỔ TAY ATTT</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Hệ thống tra cứu an toàn thông tin nội bộ</p>", unsafe_allow_html=True)
    
    st.info("👈 **HƯỚNG DẪN:** Nhấn vào dấu **>** (hoặc Menu) ở góc trái bên trên và nhập mật khẩu để bắt đầu.")
    st.divider()
    st.caption("© 2026 Bản quyền thuộc về Đội ngũ Kỹ thuật")


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
    st.markdown("---")
    
    # Tải dữ liệu từ Google Sheets
    df_risk = load_data(get_sheet_url(GID_NC))
    
    if df_risk is not None:
        for _, row in df_risk.iterrows():
            # Xác định icon dựa trên mức độ
            icon = "🚨" if "Nguy hiểm" in str(row['Mức độ']) else "⚠️"
            
            # Hiển thị dạng hộp Expander
            with st.expander(f"{icon} {row['Nguy cơ']}"):
                # Trình bày nội dung biện pháp
                st.markdown("#### **Biện pháp bảo đảm:**")
                st.info(row['Biện pháp bảo đảm'])
                
                # Hiển thị mức độ bằng màu sắc
                if "Nguy hiểm" in str(row['Mức độ']):
                    st.error(f"Đánh giá rủi ro: {row['Mức độ']}")
                else:
                    st.warning(f"Đánh giá rủi ro: {row['Mức độ']}")
    else:
        st.error("Không thể tải dữ liệu. Vui lòng kiểm tra tab Nguy cơ trong Sheets!")

elif menu == "🛠️ Công cụ":
    st.header("🛠️ Trung tâm Công cụ Bảo mật")
    tab_pw, tab_link, tab_qr = st.tabs(["🔐 Mật khẩu", "🔗 Kiểm tra Link", "📷 Quét mã QR"])

    # --- TAB 1: KIỂM TRA & TẠO MẬT KHẨU ---
    with tab_pw:
        st.subheader("Kiểm tra độ mạnh mật khẩu")
        p = st.text_input("Nhập mật khẩu cần kiểm tra:", type="password")
        if p:
            # Thuật toán tính điểm
            score = 0
            if len(p) >= 8: score += 1
            if any(c.isupper() for c in p): score += 1
            if any(c.isdigit() for c in p): score += 1
            if any(c in string.punctuation for c in p): score += 1
            
            if score == 4: st.success("🔥 Mật khẩu rất mạnh! An toàn tuyệt đối.")
            elif score == 3: st.warning("⚠️ Mật khẩu khá, nên thêm ký tự đặc biệt.")
            else: st.error("🚨 Mật khẩu quá yếu! Dễ bị tấn công bẻ khóa.")
        
        st.divider()
        if st.button("Tạo mật khẩu ngẫu nhiên (12 ký tự)"):
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            new_pw = ''.join(random.choice(chars) for _ in range(12))
            st.info("Mật khẩu mới của bạn:")
            st.code(new_pw)

    # --- TAB 2: KIỂM TRA LINK (Sửa lỗi trống) ---
    with tab_link:
        st.subheader("Phân tích liên kết nghi vấn")
        url_in = st.text_input("Dán link cần kiểm tra:", placeholder="https://example.com...")
        
        if url_in:
            url_check = url_in.lower().strip()
            # Danh sách đen nhận diện nhanh
            blacklist = ["bit.ly", "tinyurl", "shopee", "larksuite", "naptien", "bom.so"]
            
            if any(word in url_check for word in blacklist):
                st.error("🚨 **NGUY HIỂM:** Link này chứa dấu hiệu lừa đảo hoặc rút gọn không an toàn!")
            elif not url_check.startswith("https://"):
                st.warning("⚠️ **RỦI RO:** Link không có HTTPS, dữ liệu có thể bị đánh cắp.")
            else:
                st.success("✅ **AN TOÀN:** Chưa phát hiện dấu hiệu bất thường.")
            
            # Hiển thị phân tích tên miền
            try:
                domain = url_check.split('//')[-1].split('/')[0]
                st.info(f"🔍 Tên miền gốc: **{domain}**")
            except:
                pass
        else:
            st.caption("Nhập địa chỉ web để hệ thống bắt đầu quét.")

    # --- TAB 3: QUÉT MÃ QR (Yêu cầu packages.txt) ---
    with tab_qr:
        st.subheader("Trình quét mã QR an toàn")
        from pyzbar.pyzbar import decode
        
        cam_on = st.toggle("Mở Camera")
        img_file = st.camera_input("Đưa mã QR vào khung hình", disabled=not cam_on)
        
        if img_file:
            # Giải mã
            image = Image.open(img_file)
            decoded_objects = decode(image)
            
            if decoded_objects:
                for obj in decoded_objects:
                    qr_data = obj.data.decode("utf-8")
                    st.success("✅ Đã tìm thấy nội dung:")
                    st.code(qr_data)
                    
                    # Tự động kiểm tra nếu nội dung QR là link
                    if qr_data.startswith("http"):
                        if any(w in qr_data.lower() for w in ["bit.ly", "tinyurl", "lark"]):
                            st.error("🚨 Cảnh báo: Link trong QR có dấu hiệu lừa đảo!")
            else:
                st.warning("🔍 Không tìm thấy mã QR. Hãy thử chụp lại rõ nét hơn.")

elif menu == "🚨 Khẩn cấp":
    st.header("🚨 Phản ứng Sự cố")
    st.warning("⚡ HÀNH ĐỘNG NGAY:")
    st.checkbox("1. Ngắt kết nối Internet thiết bị.")
    st.checkbox("2. Thông báo ngay cho quản trị viên kỹ thuật.")
    # Sửa lỗi Syntax tại đây bằng cách bọc markdown chuẩn
    st.markdown("[📞 GỌI HOTLINE HỖ TRỢ](tel:0378765992)", unsafe_allow_html=True)
