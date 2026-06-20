while True:
    try:
        num1 = float(input("Please enter the first number: ").replace(",", "."))
        num2 = float(input("Please enter the second number: ").replace(",", "."))
        operation = input("Please enter the operation (+, -, *, /): ")
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            result = num1 / num2
        else:
            print("Invalid operation. Please try again.")
            continue
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        continue
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        continue
    else:
        print(f"Result: {result}")
    finally:
        print("End of calculations.")
