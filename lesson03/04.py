import datetime
currentYear = datetime.datetime.now().year

birthYear = int(input("Please enter your birth year: "))
firstName = input("Please enter your first name: ")
age = currentYear - birthYear

print(f"Hello {firstName}, you are {age} years old.")