#Sort letters of string in alphabetical order
string = "Something is Wrong with this string"

def sort_string(string):

    characters = list(string)
        
    characters.sort()
        
    sorted_string = ''.join(characters)
    while ' ' in sorted_string:
        response = input("Do you want to remove spaces? (yes/no): ")

        if response.lower() == "yes" or response.lower() == "y":
            sorted_string = sorted_string.replace(' ', '')
        else:
            return sorted_string
    while sorted_string.islower() == False:
        response = input("Do you want to convert all letters to lowercase? (yes/no): ")

        if response.lower() == "yes" or response.lower() == "y":
            sorted_string = sorted_string.lower()
            sort_string = list(sorted_string)
            sort_string.sort()
            sorted_string = ''.join(sort_string)

        else:
            return sorted_string
    
    return sorted_string
print(sort_string(string))