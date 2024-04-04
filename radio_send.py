import microbit
from microbit import ticks_ms
import radio


class Food:
    def __init__(self):
        self.food_items = {
            "Apple": 52,
            "Banana": 89,
            "Orange": 47,
            "Peach": 59,
            "Grapes": 69,
            "Carrot": 41,
            "Broccoli": 34,
            "Potato": 77,
            "Salmon": 208,
            "Chicken Breast": 165,
            "Pasta": 158,
            "Rice": 130,
            "Bread": 265,
            "Cheese": 402,
            "Egg": 78,
            "Yogurt": 159,
            "Milk": 42,
            "Almonds": 576,
            "Olive Oil": 884,
        }


class myRadio:
    def __init__(self, channel: int = 9):
        radio.on()
        radio.config(channel=channel)

    def send_data(self, data):
        radio.send(data)

    def set_load(self, data):
        return "&".join(data.items())


class Program:
    def __init__(self, weight: float):
        self.weight: float = weight
        self.reps = 0
        self.radio = myRadio()
        self.math = Math()

    def get_reps(self):
        current_state = "up"
        threshold_down = -500
        threshold_up = 500
        time_constraint = 1000
        last_rep_time = 0

        while True:
            z_acceleration = microbit.accelerometer.get_z()

            newtons = self.math.to_newtons(z_acceleration, weight=self.weight)
            watts = self.math.to_watts(z_acceleration, weight=self.weight)
            joules = self.math.to_joules(newtons)
            kcal = self.math.to_kcal(joules)
            food = self.math.find_closest_food(kcal)
            data = self.radio.set_load(
                {
                    "newtons": newtons,
                    "watts": watts,
                    "joules": joules,
                    "kcal": kcal,
                    "food": food,
                    "reps": self.reps,
                }
            )
            self.radio.send_data(data)

            if current_state == "up" and z_acceleration < threshold_down:
                current_state = "down"
            elif current_state == "down" and z_acceleration > threshold_up:
                current_state = "up"
                current_time = ticks_ms()
                if current_time - last_rep_time >= time_constraint:
                    self.reps += 1
                    last_rep_time = current_time

            if microbit.button_a.was_pressed():
                self.reps = 0


class Math:
    @staticmethod
    def to_newtons(milli_g: int, weight: float):
        return weight * (milli_g / 1000)

    @staticmethod
    def to_watts(milli_g: int, weight: float):
        return weight * (milli_g / 1000)

    @staticmethod
    def to_joules(newtons):
        return newtons * 0.25

    @staticmethod
    def to_kcal(joules):
        return joules * 4184

    @staticmethod
    def find_closest_food(kcal: float):
        food = Food()
        closest_food = min(
            food.food_items.keys(), key=lambda x: abs(food.food_items[x] - kcal)
        )
        return closest_food


if __name__ == "__main__":
    program = Program(0.5)
    program.get_reps()
