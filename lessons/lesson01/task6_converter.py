print("Welcome to the number converter!")

number = int(input("Please enter a number: "))

print(f"Binary: {bin(number)[2:]}")
print(f"Hexadecimal: {hex(number)[2:].upper()}")