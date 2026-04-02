import datetime
print("Hello, how are you doing?")
print("I hope you are doing well.")
name = input("What is your name?")
print("Hello, " + name + "!")
age = int(input("What is your birth year?"))
currentYear = datetime.datetime.now().year
print("You are " + str(currentYear - age) + " years old.")