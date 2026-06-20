from string import ascii_uppercase, digits


class PasswordValidationError(Exception):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("\n".join(errors))


def validating(code: str) -> bool:
    errors: list[str] = []

    if len(code) < 8:
        errors.append("Password should have at least 8 characters.")

    if not any(char in ascii_uppercase for char in code):
        errors.append("Password should contain at least one uppercase letter.")

    if not any(char in digits for char in code):
        errors.append("Password should contain at least one digit.")

    if errors:
        raise PasswordValidationError(errors)

    return True


try:
    print(validating("ghjuytrf"))
except PasswordValidationError as pve:
    print(f"""
{pve}
""")

try:
    print(validating("hgt5"))
except PasswordValidationError as pve:
    print(f"""
{pve}
""")

try:
    print(validating("Guy6"))
except PasswordValidationError as pve:
    print(f"""
{pve}
""")

try:
    print(validating("Gu763sdkh"))
except PasswordValidationError as pve:
    print(f"""
{pve}
""")
