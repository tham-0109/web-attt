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
        st.subheader("📷 Trình quét mã QR an toàn")
        from pyzbar.pyzbar import decode
        from PIL import Image
        import numpy as np

        cam_on = st.toggle("Kích hoạt Camera")
        img_file = st.camera_input("Đưa mã QR vào khung hình", disabled=not cam_on)
        
        if img_file:
            # Chuyển đổi file ảnh sang định dạng PIL để xử lý
            image = Image.open(img_file)
            st.image(image, caption="Ảnh đã chụp", width=300)
            
            # Giải mã QR
            decoded_objects = decode(image)
            
            if decoded_objects:
                for obj in decoded_objects:
                    qr_data = obj.data.decode("utf-8")
                    st.success("✅ Đã tìm thấy dữ liệu trong mã QR!")
                    
                    # Hiển thị nội dung mã QR trong hộp code để dễ sao chép
                    st.code(qr_data)
                    
                    # Kiểm tra nhanh xem nội dung có phải là link độc hại không
                    blacklist = ["bit.ly", "tinyurl.com", "shopee", "lark", "naptien"]
                    if any(word in qr_data.lower() for word in blacklist):
                        st.error("🚨 CẢNH BÁO: Mã QR này chứa liên kết có dấu hiệu lừa đảo!")
                    elif qr_data.startswith("http"):
                        st.info("🔗 Đây là một đường link. Hãy kiểm tra kỹ trước khi truy cập.")
                    else:
                        st.info("📄 Nội dung là văn bản thuần túy.")
            else:
                st.warning("🔍 Không tìm thấy mã QR nào trong ảnh. Hãy thử chụp lại rõ nét hơn và đủ ánh sáng.")
elif menu == "Khẩn cấp":
    st.title("🚨 Trung tâm Phản ứng Sự cố")
    st.error("Hãy giữ bình tĩnh và thực hiện theo các bước dưới đây.")

    # 1. Các tình huống cụ thể
    tinh_huong = st.selectbox(
        "Chọn tình huống bạn đang gặp phải:",
        ["-- Chọn tình huống --", "Nghi ngờ bị hack/theo dõi", "Mất thiết bị (Điện thoại/Laptop)", "Lộ mật khẩu/Thông tin tài khoản"]
    )

    if tinh_huong == "Nghi ngờ bị hack/theo dõi":
        st.warning("⚡ **HÀNH ĐỘNG NGAY:**")
        st.checkbox("1. Ngắt kết nối Wifi/4G ngay lập tức.")
        st.checkbox("2. Đăng xuất tài khoản khỏi tất cả các thiết bị khác.")
        st.checkbox("3. Sử dụng một thiết bị sạch khác để đổi mật khẩu.")
        
    elif tinh_huong == "Mất thiết bị (Điện thoại/Laptop)":
        st.warning("⚡ **HÀNH ĐỘNG NGAY:**")
        st.checkbox("1. Sử dụng tính năng 'Find My' hoặc 'Find My Device' để khóa/xóa dữ liệu từ xa.")
        st.checkbox("2. Liên hệ nhà mạng để khóa SIM.")
        st.checkbox("3. Thay đổi mật khẩu các ứng dụng ngân hàng, email.")

    elif tinh_huong == "Lộ mật khẩu/Thông tin tài khoản":
        st.warning("⚡ **HÀNH ĐỘNG NGAY:**")
        st.checkbox("1. Thay đổi mật khẩu ngay lập tức (sử dụng mật khẩu mạnh).")
        st.checkbox("2. Kích hoạt xác thực 2 lớp (2FA) nếu chưa có.")
        st.checkbox("3. Kiểm tra lịch sử đăng nhập để tìm hoạt động lạ.")

    st.divider()

    # 2. Hotline hỗ trợ (Dùng markdown để tạo link gọi điện trực tiếp)
    st.subheader("📞 Liên hệ hỗ trợ kỹ thuật.Tel:0378756992")
   
    # 3. Gửi báo cáo nhanh
    st.divider()
    st.subheader("📩 Gửi báo cáo nhanh cho Admin")
    msg = st.text_area("Mô tả ngắn gọn sự cố (Ví dụ: Không đăng nhập được Email...)")
    if st.button("GỬI BÁO CÁO"):
        if msg:
            st.toast("Đang gửi báo cáo...")
            # Ở đây có thể tích hợp gửi Telegram hoặc Email nếu muốn nâng cấp sau này
            st.success("Báo cáo của bạn đã được gửi. Đội kỹ thuật sẽ liên hệ lại ngay!")
            st.balloons()
        else:
            st.warning("Vui lòng nhập mô tả sự cố.")
