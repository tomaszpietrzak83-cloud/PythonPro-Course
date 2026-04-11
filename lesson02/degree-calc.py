unitIn =input("Please chose the degree unit you want to convert from (C/F/K):").upper()
unitOut =input("Please chose the degree unit you want to convert to (C/F/K):").upper()
degreeIn = float(input("Please enter the degree you want to convert:"))

if unitIn == unitIn.lower() or unitOut == unitOut.lower():
    unitIn = unitIn.upper()
    unitOut = unitOut.upper()


def convertTemperatureUnitValue (fromTemp, toTemp, tempInput):

    if fromTemp == toTemp:
        print(f" You entered same units therefore no conversion needed your temperature is: {tempInput}")
    else:
        if fromTemp == "C" and toTemp == "F":
            degreeOut = tempInput * 9/5 + 32
            
        elif fromTemp == "F" and toTemp == "C":
            degreeOut = (tempInput - 32) * 5/9
            
        elif fromTemp == "C" and toTemp == "K":
            degreeOut = tempInput + 273.15
            
        elif fromTemp == "K" and toTemp == "C":
            degreeOut = tempInput - 273.15
            
        elif fromTemp == "F" and toTemp == "K":
            degreeOut = (tempInput - 32) * 5/9 + 273.15
            
        elif fromTemp == "K" and toTemp == "F":
            degreeOut = (tempInput - 273.15) * 9/5 + 32
            
        else:
            print("Invalid input. Please enter C, F, or K for the degree units.")

        print(f"{tempInput}°{fromTemp} is equal to {degreeOut}°{toTemp}")

convertTemperatureUnitValue(unitIn, unitOut, degreeIn)   