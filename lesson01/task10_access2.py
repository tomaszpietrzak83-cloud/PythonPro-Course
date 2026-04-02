hight = int(input("What is your hight? "))
withAdult = input("Are you with an adult? (yes/no) ")
if (withAdult.lower() == "yes" and hight >= 120) or (withAdult.lower() == "no" and hight >= 160):
  print("True: 'You can go to the ride!'")
else:    
  print("False: 'Sorry, you cannot go to the ride.'")
