class Worker:
    def __init__(self, name, hourly_rate):
        self.name = name
        self.hourly_rate = hourly_rate

    def calculate_salary(self, hours_worked):
        return self.hourly_rate * hours_worked


class Programmer(Worker):
    def __init__(self, name, hourly_rate, programming_languages):
        super().__init__(name, hourly_rate)
        self.programming_languages = programming_languages


programmer1 = Programmer("Alice", 50, ["Python", "JavaScript"])
hours_worked = 40
salary = programmer1.calculate_salary(hours_worked)
print(f"{programmer1.name}'s salary: ${salary}")
