class ProcessingDataError(Exception):
    pass


def writeFile(fileName, content):
    with open(fileName, "a") as txt:
        txt.write(content)


def processData(data):

    try:
        takeSurname = data["surname"]
    except KeyError as ke:
        writeFile("log.txt", f"{str(ke)} - Missing key")
        raise ProcessingDataError(f"No such key. {str(ke)}") from ke
    return takeSurname


users = {"name": "Jan", "age": 30, "active": True, "city": "New York", "student": False}

try:
    surname = processData(users)
except ProcessingDataError as pde:
    print(f"Processing error: {str(pde)}")
