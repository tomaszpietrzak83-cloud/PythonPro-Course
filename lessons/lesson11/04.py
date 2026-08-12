class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x:3}, {self.y:3})"


pointA = Point(3, 4)
pointB = Point(1, -2)
pointC = Point(-11, 5.45)
points = [pointA, pointB, pointC]
for point in points:
    print(point)
