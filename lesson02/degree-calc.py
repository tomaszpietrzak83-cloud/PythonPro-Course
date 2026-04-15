try:
    expectedValues = ("K", "F", "C")
    unitIn = input(
        "Please chose the degree unit you want to convert from (C/F/K):"
    ).upper()
    unitOut = input(
        "Please chose the degree unit you want to convert to (C/F/K):"
    ).upper()

    if (unitIn not in expectedValues) or (unitOut not in expectedValues):
        raise ValueError

except ValueError:
    print("Please enter one of: (K/F/C).")

degreeIn = float(
    input("Please enter the degree you want to convert:").replace(",", ".")
)

try:
    if unitIn == "K" and degreeIn < 0:
        raise ValueError
    elif unitIn == "C" and degreeIn < -273.15:
        raise ValueError
    elif unitIn == "F" and degreeIn < ((degreeIn - 32) * 5 / 9 + 273.15):
        raise ValueError

except ValueError:
    print("Temperature can't be lower than absolute Zero!")
    exit()


if unitIn == unitOut:
    print(
        f" You entered same units therefore no conversion needed your temperature is: {degreeIn}"
    )


def unitToKelvin(value):
    unitInKelvin = 0
    if unitIn == "F":
        unitInKelvin = (value - 32) * 5 / 9 + 273.15
    elif unitIn == "C":
        unitInKelvin = value - 273.15
    else:
        unitInKelvin = value
    return unitInKelvin


def convertUnit(to, value):

    if to == "C":
        degreeOut = unitToKelvin(value) + 273.15
    elif to == "F":
        degreeOut = (unitToKelvin(value) + 273.15) * 9 / 5 + 32
    else:
        degreeOut = unitToKelvin(value)

    print(f"{degreeIn}°{unitIn} is equal to {degreeOut}°{to}")


convertUnit(unitOut, degreeIn)
