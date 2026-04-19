try:
    print("What is your dog's age in human years? You can use decimals.")
    dogAge = float(input("How many years old is your dog?: ").replace(",", "."))

    if dogAge >= 30:
        print("No dog can live that long.")
         
    else:

        dogAgeInHumanYears = 0

        while 0 <= dogAge < 30:
            if 0 <= dogAge < 1:
                dogAgeInHumanYears += 15 * dogAge
            elif 0 < dogAge <= 2:
                dogAgeInHumanYears += 15 + (dogAge - 1) * 9
            else:
                dogAgeInHumanYears += 24 + (dogAge - 2) * 5
            break
        print(dogAgeInHumanYears)

except:
    ValueError
    print("Please enter numerical Values.")
