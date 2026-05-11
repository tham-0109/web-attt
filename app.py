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

st.caption("Truy cập linh hoạt trên Smartphone")