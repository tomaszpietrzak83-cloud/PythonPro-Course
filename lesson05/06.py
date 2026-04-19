from random import randint

secretNumber = randint(1, 9)

while True:
    userInput = int(input("Guess number form 1 to 9  "))

    if userInput == secretNumber:
        print("Congratulation, thats right!")
        break

    print("It's not that number.")
(1,)
