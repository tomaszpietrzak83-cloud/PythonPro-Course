print("Hello, we are going to calculate the area of a rectangle!")
length = float(input("Please enter the length of the rectangle: "))
if length <= 0:
    print("Please enter a valid number for length. It should be a positive number without any letters or special characters.")
width = float(input("Please enter the width of the rectangle: "))
if width <= 0:
    print("Please enter a valid number for width. It should be a positive number without any letters or special characters.")
area = length * width
print(f"The area of the rectangle is: {area}")

