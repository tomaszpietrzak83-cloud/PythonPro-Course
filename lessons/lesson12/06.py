class InvalidPasswordError(Exception):
    pass


class PasswordTooShortError(InvalidPasswordError):
    def __init__(
        self,
        message="Password is too short. It must be at least 8 characters long.",
    ):
        super().__init__(message)


class PasswordNoUppercaseError(InvalidPasswordError):
    def __init__(
        self, message="Password must contain at least one uppercase letter."
    ):
        super().__init__(message)


def password_setter(password):
    if len(password) < 8:
        raise PasswordTooShortError()
    if not any(char.isupper() for char in password):
        raise PasswordNoUppercaseError()
    return print("Password is valid")


try:
    password_setter("short")
except (PasswordTooShortError, PasswordNoUppercaseError) as e:
    print("Error:", e)

try:
    password_setter("abitlonger")
except (PasswordTooShortError, PasswordNoUppercaseError) as e:
    print("Error:", e)

try:
    password_setter("Withuppercase")
except (PasswordTooShortError, PasswordNoUppercaseError) as e:
    print("Error:", e)
