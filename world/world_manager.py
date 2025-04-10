# world/world_manager.py
import random

from world.core.map import WorldMap
from world.entities.colony import Colony  # Добавь импорт наверху
from world.core.generator import generate_map
from world.core.conditions import WorldConditions
from world.config import MAP_WIDTH, MAP_HEIGHT, TILE_TYPES
from world.entities.object import Food


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
        self.ants = []


        self.generation = 0
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
        self.tick_count += 1

        # decay глобальных запахов
        self.world_map.scent_map.decay()

        # === Обработка ресурсов ===
        self._decay_objects()
        self._spawn_berry()
        self._spawn_random_corpse()

        # (далее можно: обновление агентов, логика поколений и т.д.)

    def get_state(self):
        """Возвращает текущее состояние мира (например, для UI или логов)"""
        return {
            "tick": self.tick_count,
            "nests": self.nest_positions,
            "conditions": self.conditions,
        }

    def _spawn_berry(self, chance=0.4):
        if random.random() > chance:
            return

        for _ in range(20):
            x, y = random.randint(0, self.world_map.width - 1), random.randint(0, self.world_map.height - 1)
            tile = self.world_map.get_tile(x, y)
            if tile.type == TILE_TYPES["GROUND"] and tile.object is None:
                from world.entities.object import Berry
                berry = Berry()
                tile.set_object(berry)
                self.world_map.scent_map.emit(x, y, scent_type="food", intensity=5)
                break

    def _spawn_random_corpse(self, chance=0.005):
        if random.random() > chance:
            return

        for _ in range(10):
            x, y = random.randint(0, self.world_map.width - 1), random.randint(0, self.world_map.height - 1)
            tile = self.world_map.get_tile(x, y)
            if tile.type == TILE_TYPES["GROUND"] and tile.object is None:
                from world.entities.object import Corpse
                corpse = Corpse(size=1.0)
                tile.set_object(corpse)
                self.world_map.scent_map.emit(x, y, scent_type="corpse", intensity=10)
                break

    def _decay_objects(self):
        for y in range(self.world_map.height):
            for x in range(self.world_map.width):
                tile = self.world_map.get_tile(x, y)
                obj = tile.object
                if isinstance(obj, Food):
                    if obj.tick_decay():
                        tile.remove_object()

    def __repr__(self):
        return f"<WorldManager tick={self.tick_count}>"
