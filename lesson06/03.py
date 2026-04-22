def average(*grades):
    total = 0
    counter = 0
    for grade in grades:
        total += grade
        counter += 1
    result = round((total / counter), 2)

    return result


def average2(*grades):
    total = 0
    total = sum(grades)
    result = round(total / len(grades), 2)
    return result


student1 = [2, 5, 6, 4, 3.5, 4.5, 1.5, 1, 2.5]
print(average(*student1))
print(average2(*student1))


student2 = [1, 2, 3, 4, 5]
print(average(*student2))
print(average2(*student2))

u = 6
v = 3
x = 2
y = 3
z = 4
print(average(u, v, x, y, z))
print(average2(u, v, x, y, z))
