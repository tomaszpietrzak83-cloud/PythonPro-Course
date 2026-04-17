names = [
    "Ann",
    "Anna",
    "Bob",
    "Cecil",
    "David",
    "Ethan",
    "Frank",
    "Gregory",
    "Helen",
    "Igor",
    "Jane",
]
userName = input("Please enter Your name: ")

found = False
for name in names:
    if name == userName:
        found = True
        print("Your name is already on the list.")
        break
if found is False:
    print("Your name is not on the list.")
