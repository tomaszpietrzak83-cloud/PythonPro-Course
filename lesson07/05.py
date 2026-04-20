from functools import reduce

numbers = [number for number in range(1, 6)]

numbersSum = reduce(lambda accumulator, number: accumulator + number, numbers)
print(numbersSum)
