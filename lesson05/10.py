buyPricesPLN = {"pln": 1, "usd": 3.5830, "eur": 4.2234, "chf": 4.5725, "gbp": 4.8442}
spreadsPLN = {"pln": 0, "usd": 0.0300, "eur": 0.0300, "chf": 0.0300, "gbp": 0.0400}


def toPLN(fromCurrency, value):
    if fromCurrency == "pln":
        return value

    return (buyPricesPLN[fromCurrency] - spreadsPLN[fromCurrency]) * value


def exchange(fromCurrency, to):
    plnAmount = toPLN(fromCurrency, amount)

    return round(plnAmount / buyPricesPLN[to], 2)


wantExit = False
while wantExit is False:
    availableCurrencies = ("pln", "usd", "eur", "chf", "gbp")
    try:
        currencyIn = input(
            f"Which currency u want to exchange: {availableCurrencies}? "
        ).lower()
        currencyOut = input(
            f"Which currency u want exchange into: {availableCurrencies}? "
        ).lower()

        if (
            currencyIn not in availableCurrencies
            or currencyOut not in availableCurrencies
        ):
            raise ValueError

        print("OK!")

    except ValueError:
        print("Chose one of PLN/USD/EUR/CHF/GBP!")
        continue

    try:
        amount = float(input("How much u want to exchange?: ").replace(",", "."))
    except ValueError:
        print("Please enter numerical values.")
        continue

    print(exchange(currencyIn, currencyOut))

    exitInput = None
    allowCommands = ("yes", "no", "y", "n")
    while exitInput not in allowCommands:
        exitInput = input("Do you want to exit?: ").lower()
        wantExit = (exitInput == "yes") or (exitInput == "y")
        if exitInput not in allowCommands:
            print("Please enter yes, no.")
