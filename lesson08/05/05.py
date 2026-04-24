def writeFile(fileName, content):
    with open(fileName, "a") as txt:
        txt.write(content)
    # txt.close totally unnecessary because with already closing file


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
    allowedOperators = ("+", "-", "*", "/")
    operator = 0
    while operator not in allowedOperators:
        try:
            operator = input("Please enter operator: ")

            if operator not in allowedOperators:
                raise ValueError

        except ValueError as ve:
            writeFile(
                "log.txt", f"{str(ve)} - Please enter one of following: *, /, +, - !"
            )
            print("Please enter one of following: *, /, +, - !")

    while True:
        try:
            firstNumber = float(
                input("Please enter the first number: ").replace(",", ".")
            )
            try:
                while operator == "/":
                    secondNumber = float(
                        input("Please enter the second number: ").replace(",", ".")
                    )
                    if secondNumber != 0:
                        break

                break
            except ZeroDivisionError as zde:
                writeFile("log.txt", f"{str(zde)} - You cant divide through zero!")
                print("You cant divide through zero!")

        except ValueError as ve:
            writeFile("log.txt", f"{str(ve)} - Please enter numerical data!")
            print("Please enter numerical data!")

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
    if exit == "Y":
        wantExit = True
