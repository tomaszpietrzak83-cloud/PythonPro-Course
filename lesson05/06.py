from random import randint

number = randint(1, 9)
guess = 0
while guess != number:
    guess = int(input("Guess number form 1 to 9  "))
    print("It's not that number.")

print("Congratulation, thats right!")
