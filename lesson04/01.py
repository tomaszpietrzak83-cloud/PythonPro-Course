print("This program will perform simple calculations on your numbers.")



while True:
    try:
        firstNumber = float(input("Please insert your first number: "))
        secondNumber = float(input("Please insert your second number: "))
    
        addition = firstNumber + secondNumber
        subtraction = firstNumber - secondNumber
        multiplying = firstNumber * secondNumber

        if secondNumber != 0:
            dividing = firstNumber / secondNumber
        else:
            dividing ="is undefined (division by zero is not allowed)."

        results = {
                    "Addition": addition, 
                    "Subtraction": subtraction,
                    "Multiplying": multiplying, 
                    "Dividing":  dividing
                }

        for operation in results:
            print(f"The result of {operation} is {results[operation]}")

    except ValueError:
        print("Invalid input. Please enter numeric values for numbers.")
    
    break