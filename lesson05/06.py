from random import randint

secretNumber = randint(1, 9)

userInput = None

while userInput != secretNumber:
    userInput = int(input("Guess number form 1 to 9  "))
    print("It's not that number.")

print("Congratulation, thats right!")
