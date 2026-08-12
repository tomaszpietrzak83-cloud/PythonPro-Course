text = """
Tom walked into the quiet forest at dawn. 
He carried a small notebook and a pen. 
The air was cold, and birds were singing. 
He wrote about everything he saw around him. 
Suddenly something moved between the tall trees. 
He stopped and listened very carefully to the silence. Night fell."""

userText = input(
    "Please enter a sentence, or press enter for example sentence: "
)

vowels = "aeiouyAEIOUY"


def deleteVowels(text):
    newSentence = ""
    for character in text:
        if character in vowels:
            continue
        newSentence += character
    return newSentence


def deleteNonVowels(text):
    newSentence = ""
    for character in text:
        if character not in vowels:
            newSentence += character
    return newSentence


question = input("Do you want to delete vowels or non-vowels? (v/n): ")

if question == "v":
    print(deleteVowels(text if userText == "" else userText))
elif question == "n":
    print(deleteNonVowels(text if userText == "" else userText))
