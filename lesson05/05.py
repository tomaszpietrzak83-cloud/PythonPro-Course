results = [
    [],
    [],
    [],
    [],
    [],
]

for i in range(1, 6):
    for j in range(1, 6):
        results[i - 1].append(i * j)

for row in results:
    print(row)
