class InvalidPasswordError(Exception):
    pass


def passwordSetter(password):
    if len(password) < 8:
        raise InvalidPasswordError("Password must be at least 8 characters long.")


try:
    passwordSetter("short")

except InvalidPasswordError as e:
    print("Error:", e)
