def createPerson(name, **additionalData):
    """Create a dictionary with a name and any extra key/value data."""
    person = {"name": name}
    person.update(additionalData)
    return person


exampleDict = createPerson("Alice", age=30, city="London", email="alice@example.com")
print(exampleDict)
