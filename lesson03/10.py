name = input("Please enter your name (it can be lowercase): ")
changedName = name.title().strip()
print(f"Your name is: {changedName}")
print(f"The length of your name string is: {len(changedName)}, and it was: {len(name)}")