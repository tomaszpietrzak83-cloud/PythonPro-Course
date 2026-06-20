class Date:
    def __init__(self, day, month, year):
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)

    def fromString(self, date_string):
        day, month, year = date_string.split("-")
        return Date(day, month, year)


date_string = "12-05-2021"
date = Date(0, 0, 0).fromString(date_string)
print(date.day)
print(date.month)
print(date.year)
