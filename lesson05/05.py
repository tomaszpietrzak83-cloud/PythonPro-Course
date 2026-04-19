results = [
    [],
    [],
    [],
    [],
    [],
]

for x in range(1, 6):
    for y in range(1, 6):
        results[x - 1].append(x * y)

for row in results:
    print(row)
