print("Hello, and welcome into simple rectangle circumference calculator!")

while True:
    try:
        length = float(input("Please enter the length of the rectangle: "))
        if length <= 0:
            print("Length must be a positive number. Please try again.")
            continue
        break
    except ValueError:
        print("Please enter a valid number.")

while True:
    try:
        width = float(input("Please enter the width of the rectangle: "))
        if width <= 0:
            print("Width must be a positive number. Please try again.")
            continue
        break
    except ValueError:
        print("Please enter a valid number.")

circumference = 2 * (length + width)
print(f"The circumference of the rectangle is: {circumference}")