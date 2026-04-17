def calculations(a, b, symbol):
    if symbol == "*":
        return a * b
    elif symbol == "/":
        return a / b
    elif symbol == "+":
        return a + b
    else:
        return a - b


wantExit = False
while wantExit is False:
    try:
        firstNumber = float(input("Please enter the first number: ").replace(",", "."))
        secondNumber = float(
            input("Please enter the second number: ").replace(",", ".")
        )

    except ValueError:
        print("Please enter numerical data!")

    try:
        operator = input("Please enter operator: ")

        allowedOperators = ("+", "-", "*", "/")
        if operator not in allowedOperators:
            raise ValueError

    except ValueError:
        print("Please enter one of following: *, /, +, - !")

    operation = ""
    if operator == "*":
        operation = "multiplication"
    elif operator == "/":
        operation = "division"
    elif operator == "+":
        operation = "addition"
    else:
        operation = "subtraction"

    print(
        f"The result of {operation} is {calculations(firstNumber, secondNumber, operator)}"
    )

    exit = input("Do you want to exit [Y]es or [N]o?").upper()
    if exit == "y":
        wantExit = True
