class IncorrectAge(Exception):
    pass


class NegativeAge(Exception):
    pass


def validateAge(userAge):

    if userAge < 0:
        raise NegativeAge("Age can't be negative.")
    if userAge < 18:
        raise IncorrectAge("Only age above 18 allowed.")

    return "Correct age."


try:
    age = input("Please enter you age here: ")
    age = int(age)

    print(validateAge(age))


except NegativeAge:
    print("Please enter only positive numbers.")
except ValueError:
    print("Please enter only numerical values.")
except IncorrectAge:
    print("Only adults allowed, sorry.")
