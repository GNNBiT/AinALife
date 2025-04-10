# world/entities/colony.py

import uuid

class Colony:
    def __init__(self, nest_center: tuple[int, int], color=None):
        self.id = uuid.uuid4()
        self.nest_center = nest_center  # координаты центра 3x3 гнезда
        self.color = color or (255, 0, 0)  # для отрисовки, если будет
        self.food_storage = 0
        self.ants = []  # список агентов (может быть id или объект)

    def add_food(self, amount: int):
        self.food_storage += amount

    def remove_food(self, amount: int):
        self.food_storage = max(0, self.food_storage - amount)

    def register_agent(self, agent):
        self.ants.append(agent)

    def __repr__(self):
        return f"<Colony id={self.id} food={self.food_storage} ants={len(self.ants)}>"
