print("Welcome to simple calculator!")
print("You can use +, -, *, / operations.")
while True:
    try:
        number1 = float(input("Enter first the number: "))
        operator = input("Enter the operator (+, -, *, /): ")
        number2 = float(input("Enter the second number: "))

        if operator == '+':
            result = number1 + number2
        elif operator == '-':
            result = number1 - number2
        elif operator == '*':
            result = number1 * number2
        elif operator == '/':

            attempts = 1
            while number2 == 0 and attempts >= 0:
                attempts -= 1
                print("Error: Division by zero is not allowed.")
                number2 = float(input("Enter second number: "))
            
            if number2 == 0:
                raise ZeroDivisionError

            result = number1 / number2
                    
        else:
            print("Invalid operator. Please use +, -, *, or /.")
            continue

        print(f"The result of {number1} {operator} {number2} is: {result}")
    except ValueError:
        print("Invalid input. Please enter numeric values for numbers.")
    except ZeroDivisionError:
        print("Thanks for using zero so many times")
    break