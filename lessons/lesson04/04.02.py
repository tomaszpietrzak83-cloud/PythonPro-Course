groceryList = ["butter", "milk", "apple", "bread", "chocolate"]

newString = ""
for item in groceryList:
    newString += f"-{item} "
print(newString)