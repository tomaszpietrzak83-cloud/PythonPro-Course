unitIn =(input("Please chose the degree unit you want to convert from (C/F/K):")).upper()
unitOut =input("Please chose the degree unit you want to convert to (C/F/K):").upper()
degreeIn = float(input("Please enter the degree you want to convert:"))
if unitIn == "C" and unitOut == "F":
    degreeOut = degreeIn * 9/5 + 32
    print(f"{degreeIn}°{unitIn} is equal to {degreeOut}°{unitOut}")
elif unitIn == "F" and unitOut == "C":
    degreeOut = (degreeIn - 32) * 5/9
    print(f"{degreeIn}°{unitIn} is equal to {degreeOut}°{unitOut}")
elif unitIn == "C" and unitOut == "K":
    degreeOut = degreeIn + 273.15
    print(f"{degreeIn}°{unitIn} is equal to {degreeOut}°{unitOut}")
elif unitIn == "K" and unitOut == "C":
    degreeOut = degreeIn - 273.15
    print(f"{degreeIn}°{unitIn} is equal to {degreeOut}°{unitOut}")
elif unitIn == "F" and unitOut == "K":
    degreeOut = (degreeIn - 32) * 5/9 + 273.15
    print(f"{degreeIn}°{unitIn} is equal to {degreeOut}°{unitOut}")
elif unitIn == "K" and unitOut == "F":
    degreeOut = (degreeIn - 273.15) * 9/5 + 32
    print(f"{degreeIn}°{unitIn} is equal to {degreeOut}°{unitOut}")
else:
    print("Invalid input. Please enter C, F, or K for the degree units.")