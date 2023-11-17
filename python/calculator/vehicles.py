class Vehicle:
    def get_vehicle_type(self) -> str:
        pass

    def is_toll_free_vehicle() -> bool:
        return False


class Car(Vehicle):
    def get_vehicle_type(self) -> str:
        return "Car"


class Motorbike(Vehicle):
    def get_vehicle_type(self):
        return "Motorbike"

    def is_toll_free_vehicle() -> bool:
        return True
