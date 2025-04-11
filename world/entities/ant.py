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

        self.respect = {}
        self.respect_cooldowns = {}

        self.health = 10  # базовое ХП, можно потом сделать эволюционно
        self.attack_power = 2  # сила атаки
        self.experience = 0.0  # пока не используется, но заложим на будущее

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def turn(self, direction_delta):
        """
        Повернуться влево (-1) или вправо (+1) по круговому списку направлений.
        """
        current_index = DIRECTION_LIST.index(self.facing)
        new_index = (current_index + direction_delta) % len(DIRECTION_LIST)
        self.facing = DIRECTION_LIST[new_index]

    def init_respect(self, peer_ids):
        """
        Инициализирует список уважаемых особей (без себя).
        """
        self.respect = {peer_id: 0.0 for peer_id in peer_ids if peer_id != self.id}

    def update_respect(self, peer_id, delta, current_step, cooldown=50):
        """
        Обновляет респект к другому муравью, если кулдаун прошёл.
        """
        last_step = self.respect_cooldowns.get(peer_id, -cooldown)
        if current_step - last_step >= cooldown:
            self.respect[peer_id] = self.respect.get(peer_id, 0.0) + delta
            self.respect_cooldowns[peer_id] = current_step

    def calculate_damage(self):
        """
        Возвращает величину урона, с учётом опыта и рандома.
        """
        exp_bonus = 1.0 + self.experience * 0.1  # слабое влияние опыта
        rand_factor = random.uniform(0.9, 1.1)
        return self.attack_power * exp_bonus * rand_factor

    def apply_damage(self, amount):
        """
        Применяет урон к муравью.
        """
        self.health -= amount

    def get_total_respect(self):
        """
        Возвращает общее количество респекта ко всем другим муравьям.
        """
        return sum(self.respect.values())

    def __repr__(self):
        return f"<Agent id={self.id} at=({self.x},{self.y}) energy={self.energy}>"
