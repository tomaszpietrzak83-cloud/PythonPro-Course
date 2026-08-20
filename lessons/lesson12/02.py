from datetime import date, datetime
from zoneinfo import ZoneInfo


class User:
    def __init__(self, age):
        self.age = age

    def __str__(self):
        return f"User(age={self.age})"

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if not 0 <= value <= 120:
            raise ValueError("Age must be between 0 and 120")
        self._age = value

    @classmethod
    def fromYearOfBirth(cls, year_of_birth: int) -> "User":
        today = datetime.now(ZoneInfo("Europe/Warsaw")).date()
        return cls(today.year - year_of_birth)

    @classmethod
    def fromDateOfBirth(cls, date_of_birth: date) -> "User":
        today = datetime.now(ZoneInfo("Europe/Warsaw")).date()
        age = today.year - date_of_birth.year
        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
            age -= 1
        return cls(age)

    @property
    def is_adult(self) -> bool:
        return self.age >= 18

    def birthday(self) -> None:
        self.age += 1

    def __repr__(self) -> str:
        return f"User(age={self.age})"


try:
    print(User([1, 2, 3]))
except TypeError as e:
    print(e)

test_user = User(25)
print(test_user)

user_from_year = User.fromYearOfBirth(1995)
print(user_from_year)

user_from_date = User.fromDateOfBirth(date(2000, 5, 15))
print(user_from_date)

try:
    user_too_old = User(130)
except ValueError as e:
    print(e)

try:
    print(User(-10))
except ValueError as e:
    print(e)

try:
    user_invalid_age = User("twenty")
except TypeError as e:
    print(e)

test_user.birthday()
print(test_user)

print(test_user.is_adult)
print(User(17).is_adult)
