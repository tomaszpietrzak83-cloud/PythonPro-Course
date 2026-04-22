PLN_TO_OTHER_RATE = {
    "pln": 1,
    "usd": 3.5830,
    "eur": 4.2234,
    "chf": 4.5725,
    "gbp": 4.8442,
}
AVAILABLE_CURRENCIES = set(PLN_TO_OTHER_RATE)
spreads = {"pln": 0, "usd": 0.0300, "eur": 0.0300, "chf": 0.0300, "gbp": 0.0400}


def to_pln(value, from_currency: str = "pln"):
    if from_currency == "pln":
        return value
    rate = PLN_TO_OTHER_RATE[from_currency] - spreads[from_currency]
    return rate * value


def exchange(amount, from_currency: str = "pln", to_currency: str = "pln"):
    if from_currency == to_currency:
        return amount
    pln_amount = to_pln(amount, from_currency)
    return round(pln_amount / PLN_TO_OTHER_RATE[to_currency], 2)


def get_currency(info: str = None):
    if info is None:
        info = ""
    else:
        info = " " + info
    curr = input(
        f"Select currency{info}, possible currencies {AVAILABLE_CURRENCIES}: "
    ).lower()
    if curr not in AVAILABLE_CURRENCIES:
        raise ValueError("Wrong currency! Possible currencies: PLN/USD/EUR/CHF/GBP!")
    return curr


def ask_exit():
    "Returns True if user wants to exit, False otherwise."
    while True:
        want_exit = input("Do you want to exit (y/n)?: ").lower()
        if want_exit not in "yn":
            print("Please enter yes, no.")
        elif want_exit == "y":
            return True
        else:
            return False


wantExit = False
while wantExit is False:
    error_flag = False
    try:
        currencyIn = get_currency("src")
        currencyOut = get_currency("dst")
    except ValueError:
        error_flag = True
        print("Wrong currency!")

    if not error_flag:
        try:
            amount = input("How much u want to exchange?: ").replace(",", ".", 1)
            amount = float(amount)
            print(
                "you exchange",
                amount,
                currencyIn,
                "to",
                exchange(amount, currencyIn, currencyOut),
                currencyOut,
            )
        except ValueError:
            print(f"Cant parse this amount: {amount}.")
            continue
    if ask_exit():
        break
