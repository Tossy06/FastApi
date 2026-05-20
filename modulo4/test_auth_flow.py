from security import hash_password, create_access_token, verify_password, decode_token

# Simular registro
users_db = {}
email = "david@email.com"
password = "mipassword123"

users_db[email]={
    "email": email,
    "password_hash": hash_password(password),
    "role": "user",
    "active": True
}

print("Usuario registrado:", users_db[email]["email"])
print("Hash guardado:", users_db[email]["password_hash"][:30], "...")

# Simular login
password_correcto = verify_password(password, users_db[email]["password_hash"])
print("Password correcto:", password_correcto)

token = create_access_token(data={"sub": email})
print("Token generado:", token[:40], "...")

email_extraido = decode_token(token)
user = users_db.get(email_extraido)
print("Usuario autenticado:", user["email"], "| rol:", user["role"])