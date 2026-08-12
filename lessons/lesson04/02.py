a, b, c = 256, 256, 256
e, f, g = 1234567890123456789123456789, 1234567890123456789123456789, 1234567890123456789123456789

print(f"Are a, b, and c the same object? {a is b is c}")
print(f"Are e, f, and g  the same object? {e is f is g}")

print(f"Id of a is {id(a)}")
print(f"Id of b is {id(b)}")
print(f"Id of c is {id(c)}")
print(f"Id of e is {id(e)}")
print(f"Id of f is {id(f)}")
print(f"Id of g is {id(g)}")

print(f"Are Id's of a, b, and c the same? {id(a) is id(b) is id(c)}")
print(f"Are Id's of e, f, and g the same? {id(e) is id(f) is id(g)}")
