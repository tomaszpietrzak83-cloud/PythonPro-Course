# from string import ascii_lowercase, ascii_uppercase, digits


class FileNameValidationError(Exception):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("\n".join(errors))


class LineValidationError(Exception):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("\n".join(errors))


# def validateLine(line: str) -> str:
#     errors: list[str] = []

#     if any(((char in ascii_lowercase) and (char in ascii_uppercase)) for char in line):
#         errors.append("Line should't contain letters.")

#     if errors:
#         raise LineValidationError(errors)
#     return line


def validateFileName(code: str) -> str:
    errors: list[str] = []
    cleanName = code.strip()
    if cleanName == "":
        errors.append("File name cannot be empty.")

    if errors:
        raise FileNameValidationError(errors)

    return cleanName


def sumNumbersFromFile(dataFile):
    total = 0

    with open(dataFile) as txt:
        for line in txt:
            try:
                valueOfLine = int(line)
            except ValueError:
                pass

            else:
                total += valueOfLine

    return total


totalFromFile = None
fileName = None
try:
    fileName = validateFileName(input("Please enter a file name: "))
    try:
        totalFromFile = sumNumbersFromFile(fileName)
    except FileNotFoundError:
        print("File not found.")
        exit()

except FileNameValidationError as fnve:
    print(f"{fnve}")
    exit()


finally:
    print(totalFromFile)
