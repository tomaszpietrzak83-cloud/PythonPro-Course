print("Chose a character from list: Dwarf(1), Elf(2), Human(3), Orc(4), custom(5)")

userChoiceOfCharacter = str(input("Your character choice: "))
match userChoiceOfCharacter:
    case "1":
        character = "Dwarf"
    case "2":
        character = "Elf"
    case "3":
        character = "Human"
    case "4":
        character = "Orc"
    case _:
        character = input("Your character race: ")
print("You chose: " + character)

print("Chose class: Warrior(1), Mage(2), Archer(3), custom(4)")

userChoiceOfCharacterClass = input("Your class choice: ")

match userChoiceOfCharacterClass:
    case "1":
        characterClass = "Warrior"
    case "2":
        characterClass = "Mage"
    case "3":
        characterClass = "Archer"
    case _:
        characterClass = str(input("Your character class: "))
print("You chose: " + characterClass)

print("You created a " + characterClass + " " + character)