# TASK 05
from faker import Faker

fake = Faker("pl_PL")
fake_en = Faker("en_US")

number_of_examples = 4


print("Names:")
for _ in range(number_of_examples):
    print(fake.name())

print("\nSentences:")
for _ in range(number_of_examples):
    print(fake_en.sentence())

print("\nAddresses:")
for _ in range(number_of_examples):
    print(fake.address())

print("\nParagraphs:")
for _ in range(number_of_examples):
    print(fake_en.paragraph())

print("\nDates:")
for _ in range(number_of_examples):
    print(fake.date_of_birth(minimum_age=18, maximum_age=65))

print("\nEmails:")
for _ in range(number_of_examples):
    print(fake.email())

print("\nPhone Numbers:")
for _ in range(number_of_examples):
    print(fake.phone_number())
