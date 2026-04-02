print("Welcome to simple calculator!")
print("You can use +, -, *, / operations.")
while True:
    try:
        number1 = float(input("Enter first number: "))
        operator = input("Enter operator (+, -, *, /): ")
        number2 = float(input("Enter second number: "))

        if operator == '+':
            result = number1 + number2
        elif operator == '-':
            result = number1 - number2
        elif operator == '*':
            result = number1 * number2
        elif operator == '/':
            if number2 != 0:
                result = number1 / number2
            else:
                print("Error: Division by zero is not allowed.")
                number2 = float(input("Enter second number: "))
                result = number1 / number2
        else:
            print("Invalid operator. Please use +, -, *, or /.")
            continue

        print(f"The result of {number1} {operator} {number2} is: {result}")
    except ValueError:
        print("Invalid input. Please enter numeric values for numbers.")