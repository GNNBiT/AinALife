# world/world_manager.py

from world.core.map import WorldMap
from world.entities.colony import Colony  # Добавь импорт наверху
from world.core.generator import generate_map
from world.core.conditions import WorldConditions
from world.config import MAP_WIDTH, MAP_HEIGHT

class WorldManager:
    def __init__(self, colony_count=1, width=MAP_WIDTH, height=MAP_HEIGHT):
        self.width = width
        self.height = height
        self.colony_count = colony_count

        # Явно объявляем поля
        self.world_map = None
        self.nest_positions = []
        self.conditions = None
        self.tick_count = 0

        self.colonies = []
        self.reset_world()

    def reset_world(self):
        self.world_map, self.nest_positions = generate_map(
            self.width, self.height, self.colony_count
        )
        self.conditions = WorldConditions()
        self.tick_count = 0
        # Здесь позже появятся: агенты, объекты, логи, поколение и т.д.
        for i, nest in enumerate(self.nest_positions):
            color = (255, 0, 0) if i == 0 else (0, 0, 255)  # можно потом сделать динамику
            colony = Colony(nest_center=nest, color=color)
            self.colonies.append(colony)

    def step(self):
        # Пока просто увеличиваем счётчик времени
        self.tick_count += 1
        # Позже сюда подключим movement, perception и т.д.

    def get_state(self):
        """Возвращает текущее состояние мира (например, для UI или логов)"""
        return {
            "tick": self.tick_count,
            "nests": self.nest_positions,
            "conditions": self.conditions,
        }

    def __repr__(self):
        return f"<WorldManager tick={self.tick_count}>"
