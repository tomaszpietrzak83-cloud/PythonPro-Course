def factorial(n: int):
    result = 1
    while n > 0:
        result *= n
        n -= 1

    return result


print(factorial(6))


def factorial2(n: int):

    result = 1 * n
    n -= 1
    if n == -1:
        return 1
    else:
        return result * factorial2(n)


print(factorial2(6))


def factorial3(n):
    if n == 0:
        return 1
    return n * factorial3(n - 1)


print(factorial3(6))
