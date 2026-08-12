class Date:
    def __init__(self, day, month, year):
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)

    def __str__(self):
        return f"Date: {self.day:02d}-{self.month:02d}-{self.year}"

    @property
    def day_text(self):
        return f"The day is {self.day:02d}"

    @property
    def month_text(self):
        return f"The month is {self.month:02d}"

    @property
    def year_text(self):
        return f"The year is {self.year}"

    @classmethod
    def fromString(cls, date_string):
        day, month, year = date_string.split("-")
        return cls(day, month, year)


date_string = "8-05-2021"
date = Date.fromString(date_string)
print(date.day_text)
print(date.month_text)
print(date.year_text)
print(date)
