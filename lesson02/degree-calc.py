unitIn = input("Please chose the degree unit you want to convert from (C/F/K):").upper()
unitOut = input("Please chose the degree unit you want to convert to (C/F/K):").upper()
degreeIn = float(
    input("Please enter the degree you want to convert:").replace(",", ".")
)

if unitIn == unitIn.lower() or unitOut == unitOut.lower():
    unitIn = unitIn.upper()
    unitOut = unitOut.upper()


def convertUnit(fromIn, to, value):

    if fromIn == to:
        print(
            f" You entered same units therefore no conversion needed your temperature is: {value}"
        )
    else:
        if fromIn == "C" and to == "F":
            degreeOut = value * 9 / 5 + 32

        elif fromIn == "F" and to == "C":
            degreeOut = (value - 32) * 5 / 9

        elif fromIn == "C" and to == "K":
            degreeOut = value + 273.15

        elif fromIn == "K" and to == "C":
            degreeOut = value - 273.15

        elif fromIn == "F" and to == "K":
            degreeOut = (value - 32) * 5 / 9 + 273.15

        elif fromIn == "K" and to == "F":
            degreeOut = (value - 273.15) * 9 / 5 + 32

        else:
            print("Invalid input. Please enter C, F, or K for the degree units.")

        print(f"{value}°{fromIn} is equal to {degreeOut}°{to}")


convertUnit(unitIn, unitOut, degreeIn)
