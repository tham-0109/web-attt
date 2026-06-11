import bcrypt
import toml

# Demo password: "demo123"
password = b"demo123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)

secrets_data = {
    "id_google_sheet": "1LeBKhdqtsmg0TwjjYuhl_N0dnsCoFEsfrU1YXxSbkOk",
    "id_tab_dieucam": "0",
    "id_tab_nguyco": "0",
    "password_hash": hashed.decode('utf-8')
}

with open(".streamlit/secrets.toml", "w", encoding="utf-8") as f:
    toml.dump(secrets_data, f)

print("✅ secrets.toml đã được tạo thành công!")
print("Mật khẩu demo: demo123")
