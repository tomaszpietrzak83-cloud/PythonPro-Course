buyPricesPLN = {"usd": 3.5830, "eur": 4.2234, "chf": 4.5725, "gbp": 4.8442}
spreadsPLN = {"usd": 0.0300, "eur": 0.0300, "chf": 0.0300, "gbp": 0.0400}


def currencyToPLN(currencyFrom, value):
    sell = 0
    if currencyFrom == "U":
        sell = (buyPricesPLN["usd"] - spreadsPLN["usd"]) * value
    elif currencyFrom == "E":
        sell = (buyPricesPLN["eur"] - spreadsPLN["eur"]) * value
    elif currencyFrom == "C":
        sell = (buyPricesPLN["chf"] - spreadsPLN["chf"]) * value
    elif currencyFrom == "G":
        sell = (buyPricesPLN["gbp"] - spreadsPLN["gbp"]) * value
    else:
        sell = value
    return sell


def currencyExchange(to):
    buy = 0
    plnAmount = currencyToPLN(currencyIn, amount)
    if to == "U":
        buy = plnAmount / buyPricesPLN["usd"]
    elif to == "E":
        buy = plnAmount / buyPricesPLN["eur"]
    elif to == "C":
        buy = plnAmount / buyPricesPLN["chf"]
    elif to == "G":
        buy = plnAmount / buyPricesPLN["gbp"]
    else:
        buy = plnAmount
    buy = round(buy, 2)
    return buy


wantExit = False
while wantExit is False:
    properCurrencies = ("P", "U", "E", "C", "G")
    try:
        currencyIn = input(
            "Which currency u want to exchange: [P]LN, [U]SD, [E]UR, [C]HF, [G]BP? "
        ).upper()
        currencyOut = input(
            "Which currency u want exchange into: [P]LN, [U]SD, [E]UR, [C]HF, [G]BP? "
        ).upper()
        if (currencyIn and currencyOut) not in (properCurrencies):
            raise ValueError
    except ValueError:
        print("Chose one of P/U/E/C/G!")

    try:
        amount = float(input("How much u want to exchange?: ").replace(",", "."))
    except ValueError:
        print("Please enter numerical values.")

    print(currencyExchange(currencyOut))

    try:
        exit = input("Do you want to exit?: ").lower()
        wantExit = exit == "yes"
    except ValueError:
        print("Please enter yes, no.")
