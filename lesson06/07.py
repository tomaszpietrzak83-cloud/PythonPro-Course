def analyze(numbers: list[int]):
    return (min(numbers), max(numbers), sum(numbers))


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
