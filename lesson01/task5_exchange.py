print("Hello, welcome to exchange!")
usdCourseInZloty = 4.0
print(f"Current exchange rate is {usdCourseInZloty} zloty for 1 dollar.")
amountInUsd = float(input("How many dollars do you want to exchange? "))
amountInZloty = amountInUsd * usdCourseInZloty
print(f"You will get {amountInZloty} zloty for {amountInUsd} dollars.")