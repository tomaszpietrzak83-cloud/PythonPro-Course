# TASK 05
from faker import Faker

fake = Faker("pl_PL")
fake_en = Faker("en_US")

print("Names:")
for _ in range(10):
    print(fake.name())

print("\nSentences:")
for _ in range(10):
    print(fake_en.sentence())
