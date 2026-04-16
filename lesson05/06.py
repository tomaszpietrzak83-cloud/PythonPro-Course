import random

number = random.randint(1, 9)
guess = 0
while guess != number:
    guess = int(input("Guess number form 1 to 9  "))

print("Congratulation, thats right!")
