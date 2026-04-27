def repeater(n):

    def decorator(function):
        print("This function counts executions:")

        def status(*args, **kwargs):

            for _ in range(1, n + 1):
                print()
                print(f"[{function.__name__}] execution #{_}")
                function(*args, **kwargs)
            print("\n", f"There was {n} executions.")
            return

        return status

    return decorator


@repeater(4)
def greet(name):
    print(f"Hello {name}")


greet("Tomek")
