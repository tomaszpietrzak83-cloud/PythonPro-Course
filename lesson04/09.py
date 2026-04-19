x = 10

print(id(x))
print("The id points to a specific object in memory.")

x += 1

print(id(x))
print("Integers are immutable, so when we add 1, x now points to a new object." )