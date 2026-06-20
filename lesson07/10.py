users = [
    {"name": "Jan", "age": 30, "active": True},
    {"name": "Anna", "age": 17, "active": False},
    {"name": "John", "age": 25, "active": True},
    {"name": "Thomas", "age": 12, "active": True},
]
print(
    list(
        map(
            lambda user: user["name"].upper(),
            filter(
                (lambda user: user["active"]) and (lambda user: user["age"] > 18), users
            ),
        )
    )
)
