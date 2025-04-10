# world/entities/object.py

import uuid

from world.config import ENERGY_GAIN_PER_FOOD


class WorldObject:
    def __init__(self, obj_type: str, weight: float = 1.0):
        self.id = uuid.uuid4()
        self.type = obj_type  # "food", "stick", "corpse"
        self.weight = weight

    def __repr__(self):
        return f"<{self.__class__.__name__} type={self.type} weight={self.weight}>"

# === Заглушки объектов ===

class Food(WorldObject):
    def __init__(self, nutrition=ENERGY_GAIN_PER_FOOD):
        super().__init__("food", weight=0.5)
        self.nutrition = nutrition


class Stick(WorldObject):
    def __init__(self, size=1.0):
        super().__init__("stick", weight=size)

class Corpse(WorldObject):
    def __init__(self, size=1.0):
        super().__init__("corpse", weight=size)
        self.decay = 1.0  # степень разложения (позже пригодится)
