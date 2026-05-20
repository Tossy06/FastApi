from security import create_access_token, decode_token

token = create_access_token(data={"sub": "david@email.com"})
print("Token Generado")
print(token)
print()

email = decode_token(token)
print("Email extraído del token:", email)