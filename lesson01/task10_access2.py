hight = int(input("What is your hight? "))
isWithAdult = input("Are you with an adult? (yes/no) ").lower() == "yes"
if (isWithAdult and 160 > hight >= 120) or (hight >= 160):
  print("True: 'You can go to the ride!'")
else:    
  print("False: 'Sorry, you cannot go to the ride.'")
