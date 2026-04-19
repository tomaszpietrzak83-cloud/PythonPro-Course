buyPricesPLN = {"usd": 3.5830, "eur": 4.2234, "chf": 4.5725, "gbp": 4.8442}
spreadsPLN = {"usd": 0.0300, "eur": 0.0300, "chf": 0.0300, "gbp": 0.0400}


def toPLN(fromCurrency, value):
    if fromCurrency == "P":
        return value

    return (buyPricesPLN[fromCurrency] - spreadsPLN[fromCurrency]) * value


def exchange(to):
    plnAmount = toPLN(currencyIn, amount)

    return round(plnAmount / buyPricesPLN[to], 2)


wantExit = False
while wantExit is False:
    availableCurrencies = ("pln", "usd", "eur", "chf", "gbp")
    try:
        currencyIn = input(
            "Which currency u want to exchange: PLN, USD, EUR, CHF, GBP? "
        ).lower()
        currencyOut = input(
            "Which currency u want exchange into: PLN, USD, EUR, CHF, GBP? "
        ).lower()

        if (currencyIn and currencyOut) not in (availableCurrencies):
            raise ValueError

    except ValueError:
        print("Chose one of PLN/USD/EUR/CHF/GBP!")

    try:
        amount = float(input("How much u want to exchange?: ").replace(",", "."))
    except ValueError:
        print("Please enter numerical values.")
        continue

    print(exchange(currencyOut))

    try:
        exit = input("Do you want to exit?: ").lower()
        wantExit = exit == "yes"
    except ValueError:
        print("Please enter yes, no.")
