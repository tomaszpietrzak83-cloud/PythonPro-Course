number = "5.8" #this is a string
print(number) # Output: 5.8
print(type(number)) # Output: <class 'str'>
number = float(number) #convert string to float
print(number) # Output: 5.8
print(type(number)) # Output: <class 'float'>
number = int(number) #convert float to int
print(number) # Output: 5 It always rounds down when converting from float to int
print(type(number)) # Output: <class 'int'>
