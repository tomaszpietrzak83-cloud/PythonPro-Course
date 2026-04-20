def isPrimeMax30(integer):
    isPrime = False
    divisionCounter = 0
    counter = 1
    for _ in range(1, 31):
        if integer % counter == 0:
            divisionCounter += 1
        counter += 1
    if divisionCounter == 2:
        isPrime = True
        return isPrime


integers = [number for number in range(1, 31)]

primeIntegers = [list(filter(lambda number: isPrimeMax30(number), integers))]
print(primeIntegers)
