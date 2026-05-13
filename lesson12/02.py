class User:
    def __init__(self, age):
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if 120 >= value >= 0:
            self._age = value

        else:
            print("Age must be between 0 and 120")
