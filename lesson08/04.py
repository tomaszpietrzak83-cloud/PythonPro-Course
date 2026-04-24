def average2(argsList):

    assert argsList != [], "List can't be empty."

    total = sum(argsList)
    result = round(total / len(argsList), 2)

    return result


student1 = [2, 5, 6, 4, 3.5, 4.5, 1.5, 1, 2.5]

print(average2(student1))
average2([])
