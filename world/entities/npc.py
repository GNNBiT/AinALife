# world/entities/npc.py

import uuid
import random

class NPC:
    def __init__(self, npc_type: str, x: int, y: int):
        self.id = uuid.uuid4()
        self.type = npc_type  # "spider", "beetle", "lizard", etc.
        self.x = x
        self.y = y

        # Простейшие параметры, которые могут пригодиться
        self.health = 100
        self.vision_range = 5
        self.patrol_range = 3

        # Можно расширить позже (например: "patrol", "chase", "idle")
        self.state = "idle"

    def get_position(self):
        return self.x, self.y

    def step(self, world_map):
        """Пока просто заглушка"""
        # В будущем: логика патрулирования или атаки
        pass

    def __repr__(self):
        return f"<NPC {self.type} at=({self.x},{self.y}) state={self.state}>"
