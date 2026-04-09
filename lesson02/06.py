age = int(input("what is your age? "))
drivingLicense = input("do you have a driving license? (yes/no) ")

storeBool = age >= 18 and drivingLicense == "yes"
print(storeBool)