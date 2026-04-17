def average(*grades):
    sum = 0
    counter = 0
    for grade in grades:
        sum += grade
        counter += 1
    result = round((sum / counter), 2)

    return result


student1 = [2, 5, 6, 4, 3.5, 4.5, 1.5, 1, 2.5]
print(average(*student1))

student2 = [1, 2, 3, 4, 5]
print(average(*student2))

u = 6
v = 3
x = 2
y = 3
z = 4
print(average(u, v, x, y, z))
