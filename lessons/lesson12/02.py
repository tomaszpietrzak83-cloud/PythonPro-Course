from datetime import date, datetime
from zoneinfo import ZoneInfo


class User:
    def __init__(self, age):
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if not 0 <= value <= 120:
            raise ValueError("Age must be between 0 and 120")
        self._age = value

    @age.getter
    def age(self):
        return self._age

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
