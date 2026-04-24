def readFile(fileName):
    with open(fileName) as txt:
        contents = txt.read()
    return contents


try:
    insides = readFile("text.txt")
except PermissionError:
    print("Permission denied!")
except FileNotFoundError:
    print("No such file!")
