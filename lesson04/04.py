groceryList = ["butter", "milk", "apple", "bread", "chocolate"]

groceryListToString = str(groceryList)

newString = ""
for character in groceryListToString:
    
    if character in ("[", "]", "'"):
        continue
    newString += character

print(newString)