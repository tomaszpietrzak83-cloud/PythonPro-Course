PI = 3.14159


class Shape:
    def calculate_area(self):
        pass


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def calculate_area(self):
        return self.side**2


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):

        return PI * (self.radius**2)


square = Square(4)
circle = Circle(3)
shapes = [square, circle]
for shape in shapes:
    print(f"Area: {shape.calculate_area():.2f}")
