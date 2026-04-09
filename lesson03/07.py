point = (10, 20, 30)
point[0] = 15
# TypeError: 'tuple' object does not support item assignment
new_point = (15, point[1], point[2])
print(new_point)  # Output: (15, 20, 30)