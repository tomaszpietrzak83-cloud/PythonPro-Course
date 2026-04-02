print("Chose a character from list: Dwarf(1), Elf(2), Human(3), Orc(4), else(5)")

character = str(input("Your character choice: "))
if character == "1":
    character = "Dwarf"
elif character == "2":
    character = "Elf"
elif character == "3":
    character = "Human"
elif character == "4":
    character = "Orc"
else:
    character = str(input("Your character race: "))
print("You chose: " + character)

print("Chose class: Warrior(1), Mage(2), Archer(3), else(4)")
characterClass = str(input("Your class choice: "))
if characterClass == "1":
    characterClass = "Warrior"
elif characterClass == "2":
    characterClass = "Mage"
elif characterClass == "3":
    characterClass = "Archer"
else:
    characterClass = str(input("Your character class: "))
print("You chose: " + characterClass)

print("You created a " + characterClass + " " + character)