# world/entities/ant.py

from world.config import STARTING_ENERGY, VISION_RANGE, SCENT_RADIUS, DIRECTION_LIST
import random
import uuid

class Ant:
    def __init__(self, x, y, colony_id=0):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.colony_id = colony_id

        self.energy = STARTING_ENERGY
        self.hunger = 0  # чем выше — тем хуже

        # Сенсоры
        self.vision_range = VISION_RANGE
        self.scent_radius = SCENT_RADIUS

        # Направление взгляда (вектор из config)
        self.facing = random.choice(DIRECTION_LIST)

        # Статусы (будут расширяться: fatigue, stress, и т.п.)
        self.status = {
            "carrying": None,  # если несёт объект (ветку/еду)
        }

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def turn(self, direction_vector):
        """Повернуться (пока без ограничений)"""
        self.facing = direction_vector

    def __repr__(self):
        return f"<Agent id={self.id} at=({self.x},{self.y}) energy={self.energy}>"
