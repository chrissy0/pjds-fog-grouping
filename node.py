import uuid


class Node:
    def __init__(self, cpu_power, storage_byte, ram_byte, latitude, longitude):
        self.id = str(uuid.uuid4())
        self.cpu_power = cpu_power
        self.storage_byte = storage_byte
        self.ram_byte = ram_byte
        self.location = {
            "latitude": latitude,
            "longitude": longitude
        }


    def update_location(self, latitude, longitude):
        self.location = {
            "latitude": latitude,
            "longitude": longitude
        }


    def get_info(self):
        return {
            "id": self.id,
            "cpu_power": self.cpu_power,
            "storage_byte": self.storage_byte,
            "ram_byte": self.ram_byte,
            "location": self.location
        }
