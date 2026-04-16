age = 56
name = "Alex"
grades = [4.5, 3.8, 5.0]
average = sum(grades) / len(grades)
status = "student"
isStudent = status == "student"

data = [age, name, average, isStudent]

for position in data:
    print(position, type(position))
