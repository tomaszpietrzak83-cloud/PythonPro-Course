exampleWord = "alphabet"

word = input("Please enter a word, or press enter for example word: ")


def letterIndexShower(phrase):
    for character in enumerate(phrase):
        print(character)


if word == "":
    letterIndexShower(exampleWord)
else:
    letterIndexShower(word)
