print("Welcome on our ride kid!")
hight = int(input("Please enter your hight in cm: "))
if hight >= 160:
    print("You can ride!")
elif 160 > hight > 120:
    withAdult = input("You are not tall enough to ride alone. Do you have an adult with you? (yes/no): ")
    if withAdult.lower() == "yes":
        print("You can ride with an adult!")
    else:
        print("Sorry, you cannot ride.")
else:
    print("Sorry, you cannot ride.")
