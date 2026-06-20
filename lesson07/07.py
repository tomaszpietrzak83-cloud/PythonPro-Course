def login(function):
    def status(*args, **kwargs):
        print()
        print(f"Initialize {function.__name__}:")
        result = function(*args, **kwargs)
        print(f"Ended {function.__name__}:")

        return result

    return status


@login
def greet(name):
    print(f"Hello {name}")


@login
def addition(a, b):
    result = a + b
    return print(f"The result of {a} + {b} is {result}")


greet("Tomek")
addition(2, 5)
