exampleWord = "alphabet"

word = input("Please enter a word, or press enter for example word: ")


def printLettersAndIndexes(phrase):
    for character in enumerate(phrase):
        print(character)


if word == "":
    printLettersAndIndexes(exampleWord)
else:
    printLettersAndIndexes(word)
