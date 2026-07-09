try:
    points = (10, 20, 30)
    points[0] = 15
except TypeError as e:
    print(f"Error: {e}")
new_point = (15, points[1], points[2])
print(new_point)  # Output: (15, 20, 30)
