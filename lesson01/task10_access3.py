hight = int(input("What is your hight? "))
withAdult = input("Are you with an adult? (yes/no) ")

if (withAdult.lower() == "yes"):
    withAdult = True
else:    
    withAdult = False

if (withAdult and hight >= 120) or (not withAdult and hight >= 160):
  print("True: 'You can go to the ride!'")
else:    
  print("False: 'Sorry, you cannot go to the ride.'")