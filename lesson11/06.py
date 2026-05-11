class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"


vector1 = Vector2D(1, 2)
vector2 = Vector2D(3, 4)

print("Vector 1:", vector1)
print("Vector 2:", vector2)
print("Vector 1 + Vector 2:", vector1 + vector2)
print("Vector 1 - Vector 2:", vector1 - vector2)
print("Is Vector 1 equal to Vector 2?:", vector1 == vector2)
