count = int(input("How many random numbers do you want to generate (1-100)? "))
digitNumber = int(input("How many digits should each random number have (1-5)? "))
sortOrder = input("Do you want to sort the numbers in ascending or descending order? (asc(A)/desc(D)) ").lower()
if count < 1 or count > 100:
    print("Invalid input for count. Please enter a number between 1 and 100.")
elif digitNumber < 1 or digitNumber > 5:
    print("Invalid input for digit number. Please enter a number between 1 and 5.")
elif sortOrder not in ['asc', 'desc', 'a', 'd']:
    print("Invalid input for sort order. Please enter 'asc' for ascending or 'desc' for descending.")
else:
    import random

    randomNumbers = []
    for i in range(count):
        randomNumber = random.randint(10**(digitNumber - 1), 10**digitNumber - 1)
        randomNumbers.append(randomNumber)

    sortedNumbers = sorted(randomNumbers, reverse=(sortOrder == 'desc' or sortOrder == 'd'))
    print("Sorted random numbers:", sortedNumbers)