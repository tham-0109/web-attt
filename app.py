import streamlit as st
import re

# 1. CẤU HÌNH TRANG (Tối ưu cho di động)
st.set_page_config(
    page_title="Hệ thống ATTT Nội bộ",
    page_icon="🛡️",
    layout="centered"
)

# Thêm CSS để giao diện trông chuyên nghiệp hơn trên điện thoại
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #0d6efd; color: white; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_input=True)

# 2. HÀNH LANG BẢO MẬT (Chỉ bạn mới truy cập được)
# Thay '123456' bằng mật khẩu riêng của bạn
XAC_THUC = "123456" 

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("Quản trị viên")
    pw_input = st.text_input("Nhập mật khẩu hệ thống:", type="password")
    
    if pw_input != XAC_THUC:
        st.warning("Vui lòng nhập mật khẩu để mở khóa các tính năng.")
        st.stop()
    
    st.success("Đã xác thực thành công!")
    st.divider()
    menu = st.radio(
        "DANH MỤC CHÍNH",
        ("📰 Bảng tin ATTT", "🛠️ Công cụ Bảo mật", "🔍 Tra cứu CVE", "🚨 Xử lý khẩn cấp")
    )

# 3. NỘI DUNG TỪNG MENU
if menu == "📰 Bảng tin ATTT":
    st.title("📰 Tin tức & Cảnh báo")
    st.info("**Ngày cập nhật:** 11/05/2026")
    
    with st.expander("⚠️ Cảnh báo lừa đảo SMS tháng 5", expanded=True):
        st.write("""
        Hiện nay đang rộ lên chiến dịch gửi tin nhắn giả mạo ngân hàng với nội dung: 
        *'Tài khoản của bạn bị tạm khóa, vui lòng đăng nhập tại bit.ly/bank-xyz'*. 
        **Tuyệt đối không bấm vào link.**
        """)
        
    with st.expander("🛡️ Cập nhật phần mềm"):
        st.write("- **Chrome:** Đã có bản vá lỗi Zero-day, hãy cập nhật lên bản mới nhất.")
        st.write("- **Windows:** Kiểm tra Windows Update để vá lỗi bảo mật tháng 5.")

elif menu == "🛠️ Công cụ Bảo mật":
    st.title("🛠️ Công cụ kiểm tra nhanh")
    
    # Chức năng Kiểm tra Mật khẩu
    st.subheader("1. Đánh giá độ mạnh mật khẩu")
    pw = st.text_input("Nhập mật khẩu cần kiểm tra:", type="password", help="Chúng tôi không lưu trữ mật khẩu của bạn.")
    if pw:
        score = 0
        checks = {
            "Độ dài >= 8 ký tự": len(pw) >= 8,
            "Có chữ hoa & chữ thường": re.search("[a-z]", pw) and re.search("[A-Z]", pw),
            "Có số (0-9)": re.search("[0-9]", pw),
            "Có ký tự đặc biệt (@, #,...)": re.search("[@#$%^&+=!]", pw)
        }
        
        for label, met in checks.items():
            if met:
                st.write(f"✅ {label}")
                score += 1
            else:
                st.write(f"❌ {label}")
        
        if score == 4: st.success("Đánh giá: **RẤT MẠNH**")
        elif score == 3: st.warning("Đánh giá: **TRUNG BÌNH**")
        else: st.error("Đánh giá: **YẾU**")

    st.divider()

    # Chức năng Quét Link
    st.subheader("2. Phân tích link nghi vấn")
    url_input = st.text_input("Dán đường link (URL) vào đây:")
    if url_input:
        blacklist = ['bit.ly', 'tinyurl.com', 'shopee-km.com', 'quatang-online.vn', 'zalo.me.security']
        is_bad = any(x in url_input.lower() for x in blacklist)
        
        if is_bad:
            st.error("🚨 CẢNH BÁO: Link này chứa dấu hiệu lừa đảo hoặc link rút gọn độc hại!")
        else:
            st.info("💡 Link này chưa nằm trong danh sách đen, nhưng hãy kiểm tra kỹ tên miền trước khi nhập thông tin.")

elif menu == "🔍 Tra cứu CVE":
    st.title("🔍 Tra cứu lỗ hổng bảo mật")
    st.write("Tra cứu thông tin chi tiết về các lỗ hổng từ cơ sở dữ liệu NVD quốc gia.")
    
    cve_id = st.text_input("Nhập mã CVE (Ví dụ: CVE-2024-21413):")
    if cve_id:
        if re.match(r"^CVE-\d{4}-\d+$", cve_id.upper()):
            url = f"https://nvd.nist.gov/vuln/detail/{cve_id.upper()}"
            st.success(f"Đã tìm thấy mã: {cve_id.upper()}")
            st.markdown(f"👉 [Nhấn vào đây để xem chi tiết lỗ hổng trên NVD]({url})")
        else:
            st.error("Sai định dạng mã CVE (Đúng: CVE-YYYY-NNNNN)")

elif menu == "🚨 Xử lý khẩn cấp":
    st.title("🚨 Quy trình xử lý sự cố")
    st.markdown("""
    Dành cho người dùng khi gặp vấn đề về an toàn thông tin:
    
    1. **Bị hack tài khoản:**
        - Ngắt kết nối các thiết bị đang đăng nhập.
        - Đổi mật khẩu email khôi phục trước, sau đó đến tài khoản bị hack.
        - Bật xác thực 2 lớp (2FA).
        
    2. **Bấm nhầm link độc/Tải file lạ:**
        - Ngắt Wifi/4G ngay lập tức.
        - Sao lưu dữ liệu quan trọng ra ổ cứng ngoài.
        - Chạy phần mềm quét Virus (Windows Defender hoặc Kaspersky).
        
    3. **Bị lộ thông tin CCCD/Ngân hàng:**
        - Gọi lên tổng đài ngân hàng khóa thẻ tạm thời.
        - Theo dõi biến động số dư và lịch sử đăng nhập.
    """)
    st.button("📞 Gọi hỗ trợ kỹ thuật (Giả định)")

# 4. CHÂN TRANG
st.sidebar.divider()
st.sidebar.caption("Hệ thống phát triển bởi: [Tên của bạn]")
st.sidebar.caption("Phiên bản Mobile v2.0")
