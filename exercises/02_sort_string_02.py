string = "What is the best way to Sort this string?"
def sort_string(string):

    while not string.islower():
        response = input("Do you want to get rid of the capital letters? (yes/no) ")
        if response.lower() == "yes" or response.lower() == "y":
            string = string.lower()
        else:
            break
    strangeCharacters = ['!', '?', '.', ',', ';', ':', '-', '_', '(', ')', '[', ']', '{', '}', '"', "'"]
    
    while any(char in string for char in strangeCharacters):
        response = input("Do you want to get rid of the strange characters f.e. exclamation marks? (yes/no) ")
        if response.lower() == "yes" or response.lower() == "y":
            for char in strangeCharacters:
                string = string.replace(char, '')
        else:
            break
    
    stringOrList = input("Do you want to sort the string as a whole or sort the words separately? (string/words) ")
    
    if stringOrList.lower() == "words" or stringOrList.lower() == "w":
        words = string.split()
        words.sort()
        return words
    elif stringOrList.lower() == "string" or stringOrList.lower() == "s":
        pass
    else:
        print("Invalid input. Please enter 'string' or 'words'.")


    words = string.split()
    words.sort()
    sorted_string = ' '.join(words)
    return sorted_string
print(sort_string(string))