class Vehicle:
    def start_engine(self):
        print("Vehicle engine started")


class Car(Vehicle):
    def start_engine(self):
        print("Car engine started")


class Motorcycle(Vehicle):
    def start_engine(self):
        print("Motorcycle engine started")


car = Car()
motorcycle = Motorcycle()

car.start_engine()
motorcycle.start_engine()