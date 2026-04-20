def isPrime(integer):
    if integer < 2:
        return False

    for number in range(2, (int(integer**0.5) + 1)):
        if integer % number == 0:
            return False
    return True


integers = [number for number in range(1, 31)]

primeIntegers = [list(filter(lambda number: isPrime(number), integers))]
print(primeIntegers)
