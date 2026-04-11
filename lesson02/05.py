print("Chose a character from list: Dwarf(1), Elf(2), Human(3), Orc(4), custom(5)")

userChoiceOfCharacter = str(input("Your character choice: "))
if userChoiceOfCharacter == "1":
    character = "Dwarf"
elif userChoiceOfCharacter == "2":
    character = "Elf"
elif userChoiceOfCharacter == "3":
    character = "Human"
elif userChoiceOfCharacter == "4":
    character = "Orc"
else:
    character = input("Your character race: ")
print("You chose: " + character)

print("Chose class: Warrior(1), Mage(2), Archer(3), custom(4)")
userChoiceOfCharacterClass = input("Your class choice: ")
if userChoiceOfCharacterClass == "1":
    characterClass = "Warrior"
elif userChoiceOfCharacterClass == "2":
    characterClass = "Mage"
elif userChoiceOfCharacterClass == "3":
    characterClass = "Archer"
else:
    characterClass = str(input("Your character class: "))
print("You chose: " + characterClass)

print("You created a " + characterClass + " " + character)