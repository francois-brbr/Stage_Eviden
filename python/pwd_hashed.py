import bcrypt

password = b"airflow"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)
