def analyze(numbers: list[int]):
    return (min(numbers), max(numbers), sum(numbers))


def analyze2(numbers):
    minimum = None
    maximum = None
    total = 0
    for number in numbers:
        if maximum is None or number > maximum:
            maximum = number
        elif minimum is None or number < minimum:
            minimum = number
        total += number
    return (minimum, maximum, total)


exampleList = [
    2,
    11,
    45,
    55,
    11,
    12,
    41,
    25,
    36,
    62,
    54,
    78,
    958,
    147,
    225,
    554,
    12,
    4,
    2,
    5,
    6,
]

print(analyze(exampleList))
print(analyze2(exampleList))
