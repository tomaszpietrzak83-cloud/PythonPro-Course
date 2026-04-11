print("Hello, welcome to the exchange!")
usd_to_pln_rate = 4.0
print(f"Current exchange rate is {usd_to_pln_rate} zloty for 1 dollar.")
amountInUsd = float(input("How many dollars do you want to exchange? "))
amountInZloty = amountInUsd * usd_to_pln_rate
print(f"You will get {amountInZloty} zloty for {amountInUsd} dollars.")