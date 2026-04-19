#In this code there should be few comments!

# Inputs from user. Expected value is float.
base = float(input("Please enter the base of triangle: ").replace(",", "."))
height = float(input("Please enter the height of triangle: ").replace(",", "."))

def triangleArea (a, b):
    
    """
    Function returns area.

    args:
    base of triangle
    height of triangle
    no matter which is first
    
    It multiplies args, and divides by 2.
    """
    #Here is formula.
    area = a * b / 2

    #Returns area.
    return area

print(f"Area of triangle is {triangleArea(base, height)}")
print(f"Area of triangle is {triangleArea(height, base)}")