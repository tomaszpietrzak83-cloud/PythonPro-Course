def get_number(prompt):
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_operation(prompt):
    while True:
        operation = input(prompt)
        if operation in ["+", "-", "*", "/"]:
            return operation
        else:
            print("Invalid operation. Please enter one of +, -, *, /.")


def divide_numbers(num1, num2):
    try:
        return num1 / num2
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")


def change_operation_after_division():
    while True:
        new_operation = input("Please enter a new operation (+, -, *): ")
        if new_operation in ["+", "-", "*"]:
            return new_operation
        else:
            print("Invalid operation. Please enter one of +, -, *.")


def calculate(num1, num2, operation):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    else:
        return divide_numbers(num1, num2)


while True:
    num1 = get_number("Please enter the first number: ")
    num2 = get_number("Please enter the second number: ")

    operation = get_operation("Please enter the operation (+, -, *, /): ")

    while operation == "/" and num2 == 0:
        print("Error: Division by zero is not allowed.")
        operation = change_operation_after_division()

    result = calculate(num1, num2, operation)

    print(f"Result: {result:.4f}")
    print("End of calculations.")
    break
