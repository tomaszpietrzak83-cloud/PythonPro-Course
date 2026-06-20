numbers = [-5, 2, 8, -1, 0, 10, 6]

print(
    sorted(
        list(map(lambda number: number**2, filter(lambda number: number > 0, numbers)))
    )
)
