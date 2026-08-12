def getValue(dictionary, key):
    value = dictionary.get(key)
    return value


def getValue2(dictionary, key):

    try:
        value = dictionary[key]
    except KeyError as ke:
        print(f"{str(ke)} - Missing key")
        return None
    return value


users = {"name": "Jan", "age": 30, "active": True, "city": "New York", "student": False}


data = [
    getValue(users, "name"),
    getValue2(users, "name"),
    getValue(users, "email"),
    getValue2(users, "email"),
]
for _ in data:
    print(_)
