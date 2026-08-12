hight = int(input("What is your hight? "))
withAdult = input("Are you with an adult? (yes/no) ")

isWithAdult = withAdult.lower() == "yes"
canRide = (isWithAdult and (160 > hight >= 120)) or  (hight >= 160)

if canRide == True:
  print("True")
else:    
  print("False")