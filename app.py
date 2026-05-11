import streamlit as st
import re

# Tối ưu giao diện cho điện thoại
st.set_page_config(page_title="ATTT Mobile", page_icon="🛡️")

st.title("🛡️ Cổng An Toàn Thông Tin")
st.info("Ứng dụng hỗ trợ kiểm tra bảo mật nhanh.")

# Chức năng 1: Kiểm tra mật khẩu
with st.expander("🔑 Kiểm tra độ mạnh mật khẩu", expanded=True):
    pw = st.text_input("Nhập mật khẩu:", type="password")
    if pw:
        strength = "Yếu ❌"
        if len(pw) >= 8 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw):
            strength = "Mạnh ✅"
        st.write(f"Đánh giá: **{strength}**")

# Chức năng 2: Tin tức nhanh
with st.expander("📰 Cảnh báo mới nhất"):
    st.write("- ⚠️ Cảnh báo lừa đảo qua tin nhắn giả mạo ngân hàng.")
    st.write("- 🛡️ Cách bảo mật Facebook 2 lớp.")
st.divider()
st.subheader("🔍 Tra cứu lỗ hổng (CVE)")
cve_id = st.text_input("Nhập mã CVE (VD: CVE-2024-XXXX):")

if cve_id:
    # Đây là link dẫn đến cơ sở dữ liệu lỗ hổng quốc gia
    url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
    st.write(f"Xem chi tiết tại: [{cve_id}]({url})")
    st.info("Mẹo: Các mã CVE giúp bạn biết phần mềm nào đang bị lỗi để kịp thời cập nhật.")
st.caption("Truy cập linh hoạt trên Smartphone")
