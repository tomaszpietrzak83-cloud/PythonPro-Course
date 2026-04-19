baseTicketPrice = 100

examplePassengers = {
    "passenger1": {"age": 12, "student": "yes"},
    "passenger2": {"age": 15, "student": "no"},
    "passenger3": {"age": 24, "student": "yes"},
    "passenger4": {"age": 50, "student": "no"},
}

discount = 0.5

for passenger in examplePassengers:
    hasDiscount = (examplePassengers[passenger]["age"] <= 18) or (
        examplePassengers[passenger]["student"] == "yes"
    )
    print(
        f"Passenger {'has' if hasDiscount is True else "hasn't"} "
        f"got discount and price of the ticket is "
        f"{(baseTicketPrice * discount) if hasDiscount is True else (baseTicketPrice)}"
    )
