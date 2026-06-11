import bcrypt

# Demo password: demo123
password = b"demo123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print(hashed.decode('utf-8'))
