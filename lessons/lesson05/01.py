try:
    age = int(input("Please enter your age: "))
except ValueError:
    print("Please enter numerical value.")

if 0 <= age <= 1:
    print("It appears you are infant.")
elif age <= 12:
    print("You are child, carry on.")
elif age <= 17:
    print("You are teenager. Good for you.")
elif age <= 64:
    print("You'r an adult.")
else:
    print("You are a senior. Respect!")
