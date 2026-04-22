def calculations(a: float, b: float, symbol: str) -> float:
    """
    Depending on operator function:
    "+" adds a to b,
    "-" subtracts b form a,
    "*" multiplies a by b,
    "/" divides a by b,

    args a, and b.

    a is float number;
    b is float number;

    The function returns float number.
    """
    if symbol == "*":
        return a * b
    elif symbol == "/":
        return a / b
    elif symbol == "+":
        return a + b
    else:
        return a - b
