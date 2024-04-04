from microbit import *
import radio


class Radio:
    def __init__(self, channel: int = 9):
        radio.on()
        radio.config(channel=channel)
        self.data = {
            "newtons": 0,
            "watts": 0,
            "joules": 0,
            "kcal": 0,
            "food": 0,
            "reps": 0,
        }
        while True:
            self.get_data()

    def get_data(self):
        if radio.receive() is not None:
            received_data = radio.receive()
            received_data.split("&")
            self.data["newtons"] += received_data[0]
            self.data["watts"] += received_data[1]
            self.data["joules"] += received_data[2]
            self.data["kcal"] += received_data[3]
            self.data["food"] += received_data[4]
            self.data["reps"] += received_data[5]

            print()
            print("\n" * 40)
