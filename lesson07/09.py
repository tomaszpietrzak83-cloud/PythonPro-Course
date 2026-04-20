def repeater(n):

    def decorator(function):

        def status(*args, **kwargs):

            for _ in range(1, n + 1):
                print()
                print(f"[{function.__name__}] execution #{_}")
                function(*args, **kwargs)

            return

        return status

    return decorator


@repeater(3)
def greet(name):
    print(f"Hello {name}")


greet("Tomek")
