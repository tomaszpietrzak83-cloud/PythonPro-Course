baseTicketPrice = 100

examplePassengersAge = {
    "passenger1": {"age": 12, "student": "yes"},
    "passenger2": {"age": 15, "student": "no"},
    "passenger3": {"age": 24, "student": "yes"},
    "passenger4": {"age": 50, "student": "no"},
}

discount = 0.5

for passenger in examplePassengersAge:
    haveDiscount = (examplePassengersAge[passenger]["age"] <= 18) or (
        examplePassengersAge[passenger]["student"] == "yes"
    )
    print(
        f"Passenger {'have' if haveDiscount is True else "haven't"} "
        f"got discount and price of the ticket is "
        f"{(baseTicketPrice * discount) if haveDiscount is True else (baseTicketPrice)}"
    )
