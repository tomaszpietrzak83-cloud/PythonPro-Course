text = """
Tom walked into the quiet forest at dawn. 
He carried a small notebook and a pen. 
The air was cold, and birds were singing. 
He wrote about everything he saw around him. 
Suddenly something moved between the tall trees. 
He stopped and listened very carefully to the silence. Night fell."""

userText = input("Please enter a sentence, or press enter for example sentence: ")


def cutVowels(text):
    newSentence = ""
    for character in text:
        if character in ("aeiouyAEIOUY"):
            continue
        newSentence += character
    return newSentence


print(cutVowels(text) if userText == "" else cutVowels(userText))
