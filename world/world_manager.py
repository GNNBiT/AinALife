# world/world_manager.py
import random

from world.config import MAP_WIDTH, MAP_HEIGHT, TILE_TYPES

from world.core.map import WorldMap
from world.core.generator import generate_map
from world.core.conditions import WorldConditions

from world.entities.object import Food, Berry, Corpse
from world.entities.colony import Colony  # Добавь импорт наверху

from world.systems.death import check_death


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

    def reset_world(self, first_get = False):
        self.world_map, self.nest_positions, self.ants = generate_map(
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
        self._process_attacks()
        for ant in list(self.ants):  # используем list(), чтобы избежать проблем при удалении
            check_death(ant, self.world_map, self.ants)

    def get_state(self):
        """Возвращает текущее состояние мира (например, для UI или логов)"""
        return {
            "tick": self.tick_count,
            "nests": self.nest_positions,
            "conditions": self.conditions,
        }

    def _spawn_berry(self, chance=0.9):
        if random.random() > chance:
            return

        for _ in range(20):
            x, y = random.randint(0, self.world_map.width - 1), random.randint(0, self.world_map.height - 1)
            tile = self.world_map.get_tile(x, y)
            if tile.type == TILE_TYPES["GROUND"] and tile.is_empty():
                berry = Berry()
                tile.set_object(berry)

                self.world_map.scent_map.emit(
                    x, y,
                    scent_type="food",
                    colony_id=-1,  # нейтральный мир
                    intensity=5,
                    radius=6,
                    lifespan=berry.decay
                )
                break

    def _spawn_random_corpse(self, chance=0.005):
        if random.random() > chance:
            return

        for _ in range(10):
            x, y = random.randint(0, self.world_map.width - 1), random.randint(0, self.world_map.height - 1)
            tile = self.world_map.get_tile(x, y)
            if tile.type == TILE_TYPES["GROUND"] and tile.is_empty():
                corpse = Corpse(size=1.0)
                tile.set_object(corpse)
                self.world_map.scent_map.emit(
                    x, y,
                    scent_type="corpse",
                    colony_id=-1,  # нейтральный мир
                    intensity=10,
                    radius=6,
                    lifespan=corpse.decay
                )
                break

    def _decay_objects(self):
        for y in range(self.world_map.height):
            for x in range(self.world_map.width):
                tile = self.world_map.get_tile(x, y)

                for obj_type, obj in list(tile.objects.items()):
                    if isinstance(obj, Food):
                        if obj.tick_decay():
                            tile.remove_object(obj)

    def _process_attacks(self):
        """
        Обрабатывает все атаки между муравьями.
        """
        combat_pairs = []  # список (attacker, target)

        # 1. Собираем пары: кто хочет атаковать кого
        for ant in list(self.ants):  # list() на случай удаления по ходу
            action = getattr(ant, "next_action", None)
            if action and action.get("type") == "attack":
                target_id = action.get("target")
                target = next((a for a in self.ants if a.id == target_id), None)
                if target:
                    combat_pairs.append((ant, target))

        # 2. Применяем урон в обе стороны
        for attacker, target in combat_pairs:
            damage_to_target = attacker.calculate_damage()
            target.apply_damage(damage_to_target)

            # если target тоже атакует attacker — обоюдная атака
            reverse = getattr(target, "next_action", None)
            if reverse and reverse.get("type") == "attack" and reverse.get("target") == attacker.id:
                damage_to_attacker = target.calculate_damage()
                attacker.apply_damage(damage_to_attacker)

    def __repr__(self):
        return f"<WorldManager tick={self.tick_count}>"
