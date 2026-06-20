def createCounter():
    counter = 0

    def increment():
        nonlocal counter
        counter += 1
        return counter

    return increment


counter = createCounter()
counter()  # +1
counter()  # +1
counter()  # +1
counter()  # +1
counter()  # +1
counter()  # +1
print(counter())  # +1 = 7

counter2 = createCounter()
counter2()  # +1
counter2()  # +1
counter2()  # +1
print(counter2())  # +1 = 4
