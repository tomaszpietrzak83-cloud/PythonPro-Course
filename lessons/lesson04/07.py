text = "Python"

try:

    number = int(text)

except:
    ValueError
    print("You trying to convert string into integer - which is not possible.")