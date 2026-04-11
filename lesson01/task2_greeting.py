import datetime as d
print("Hello, how are you doing?")
print("I hope you are doing well.")
name = input("What is your name?")
print("Hello, " + name + "!")
birthYear = int(input("What is your birth year?"))
currentYear = d.datetime.now().year
print("You are " + str(currentYear - birthYear) + " years old.")