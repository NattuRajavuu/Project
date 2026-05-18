class person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_age(self):
        return self.age

p1 = person("Alwin", 18)
print(p1.name)
# print(p1.age) this will print the name and age of the person object p1. The get_age method is added to demonstrate encapsulation, allowing access to the age attribute through a method rather than directly.
print(p1.get_age())