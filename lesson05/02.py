def hasDiscount(age: int, student: str = "no") -> bool:
    return (age <= 18) or (student == "yes")


def passenger_info(passName, has_discount, ticket_price):
    return f"""Passenger {passName}
          discount: {has_discount},
          ticket price: {ticket_price}"""


examplePassengers = {
    "passenger1": {"age": 12, "student": "yes"},
    "passenger2": {"age": 15, "student": "no"},
    "passenger3": {"age": 24, "student": "yes"},
    "passenger4": {"age": 50, "student": "no"},
}
baseTicketPrice = 100

discount = 0.5


for passenger, data in examplePassengers.items():
    has_discount = hasDiscount(data["age"], data["student"])

    if has_discount:
        price = baseTicketPrice * discount
    else:
        price = baseTicketPrice

    print(passenger_info(passenger, has_discount, price))
