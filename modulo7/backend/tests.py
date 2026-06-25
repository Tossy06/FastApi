user_db = [
    {
        "email": "david@example.com",
        "password": "12345678",
     }
]

user_data = {
        "email": "david1@example.com",
        "password": "12345678",
     }

def register(user):
    
    for item in user_db:
        if item["email"] == user_data["email"]:
            return "El usuario ya existe"
    user_db.append(user)
    return user

print(register(user_data))