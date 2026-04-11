hight = int(input("What is your hight? "))
withAdult = input("Are you with an adult? (yes/no) ")

isWithAdult = withAdult.lower() == "yes"

if (isWithAdult and (160 > hight >= 120)) or  (hight >= 160):
  print((isWithAdult and (160 > hight >= 120)) or  (hight >= 160))
else:    
  print("False")