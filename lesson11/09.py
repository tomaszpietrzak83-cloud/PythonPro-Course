class UserRegistration:
    def __init__(self, email, password):
        errors = []

        if "@" not in email:
            errors.append("Email must contain '@' character")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        if errors:
            raise ValueError("\n ".join(errors))

        self.email = email
        self.password = password


try:
    user1 = UserRegistration("user@example.com", "password123")
    print("User1 created successfully")
except ValueError as ve:
    print(f"""
Error creating user1: {ve}""")

try:
    user2 = UserRegistration("userexample.com", "ValidPass")
    print("User2 created successfully")
except ValueError as ve:
    print(f"""
Error creating user2: {ve}""")

try:
    user3 = UserRegistration("user@example.com", "short")
    print("User3 created successfully")
except ValueError as ve:
    print(f"""
Error creating user3: {ve}""")

try:
    user4 = UserRegistration("userexample.com", "short")
    print("User4 created successfully")
except ValueError as ve:
    print(f"""
Error creating user4: {ve}""")
