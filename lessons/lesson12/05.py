try:
    with open("nonexistent_file.txt", "r") as file:
        content = file.read()
        print(content)

except FileNotFoundError:
    print("The file does not exist. Please check the file name and try again.")
