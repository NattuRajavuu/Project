class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        print("Drive!")

class Boat:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        print("Sail!")

class Plane:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        print("Fly!")

c1 = Car("Toyota", "Corolla") #create car object
b1 = Boat("Yamaha", "242X") #create boat object
p1 = Plane("Boeing", "747") #create plane object

for x in(c1, b1, p1):
    x.move() #call the move method on each object