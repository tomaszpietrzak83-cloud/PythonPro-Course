grades = {"Jan": 4, "Anna": 5, "Bob": 3, "Jane": 4}

print(grades)


sortedGradesReversed = sorted(grades, key=lambda value: grades[value], reverse=True)
print(sortedGradesReversed)
