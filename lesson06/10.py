def validating(code: str) -> bool:
    """
    Function checks code for length, upper character, and digit.

    arguments:
    code is string

    returns True if all above are true.
    """
    # first declare False
    validation = False
    # second check if length is greater than 8
    if len(code) >= 8:
        # third check if there is upper letter
        if any(char in alphabet.upper() for char in code):
            # next check if there is digit
            if any(digit in digits for digit in code):
                # if all true validation true
                validation = True
    # returns True or False
    return validation


alphabet = "abcdefghijklmnopqrstuvwxyz"
digits = "0123456789"
validation = False

exampleTexts = ["Abdgko21s", "dhfjDFGda", "2316576a", "123Ad!@#", "A1a"]

for text in exampleTexts:
    print(validating(text))
