import bcrypt
import getpass


def main():
    print("🔐 Tạo bcrypt hash cho mật khẩu hệ thống")
    password = getpass.getpass("Nhập mật khẩu bạn muốn sử dụng: ")
    password_bytes = password.encode('utf-8')
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    print("\n✅ Hash đã được tạo:")
    print(hashed.decode('utf-8'))
    
    print("\n📋 Thêm dòng sau vào secrets.toml của bạn:")
    print(f'password_hash = "{hashed.decode("utf-8")}"')


if __name__ == "__main__":
    main()
