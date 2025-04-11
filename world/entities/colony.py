# world/entities/colony.py

import uuid
from world.config import MAX_KNOWN_COLONIES

class Colony:
    def __init__(self, nest_center: tuple[int, int], color=None):
        self.id = uuid.uuid4()
        self.nest_center = nest_center  # координаты центра 3x3 гнезда
        self.color = color or (255, 0, 0)  # для отрисовки, если будет
        self.food_storage = 0
        self.ants = []  # список агентов (может быть id или объект)
        self.relationships = {}
        self._init_relationships()

    def _init_relationships(self):
        """
        Инициализирует слоты для отношений с другими колониями.
        Свою колонию не включаем.
        """
        for cid in range(MAX_KNOWN_COLONIES):
            if cid != self.id:
                self.relationships[cid] = {
                    "trust": 0.0,
                    "interactions": 0
                }

    def add_food(self, amount: int):
        self.food_storage += amount

    def remove_food(self, amount: int):
        self.food_storage = max(0, self.food_storage - amount)

    def register_agent(self, agent):
        self.ants.append(agent)

    def update_relationship(self, other_colony_id, delta_trust=0.0):
        """
        Обновляет отношения с другой колонией.
        """
        if other_colony_id in self.relationships:
            rel = self.relationships[other_colony_id]
            rel["trust"] += delta_trust
            rel["interactions"] += 1

    def get_relationship(self, other_colony_id):
        """
        Возвращает текущие отношения с другой колонией.
        """
        return self.relationships.get(other_colony_id, {"trust": 0.0, "interactions": 0})

    def __repr__(self):
        return f"<Colony id={self.id} food={self.food_storage} ants={len(self.ants)}>"
