# world/core/tile.py

from world.config import TILE_TYPES, TILE_PASSABLE, TILE_OPAQUE
from world.entities.object import Stick, Barricade


class Tile:
    def __init__(self, tile_type: int):
        self.type = tile_type
        self.passable = TILE_PASSABLE.get(tile_type, True)
        self.opaque = TILE_OPAQUE.get(tile_type, False)  # блокирует ли обзор
        self.object = None   # Еда, ветка, падаль и т.д.

    def is_empty(self) -> bool:
        """Нет объекта на клетке"""
        return self.object is None

    def can_enter(self) -> bool:
        """Можно ли наступить на тайл"""
        return self.passable and self.is_empty()

    def set_object(self, obj):
        self.object = obj

    def remove_object(self):
        self.object = None

    def place_stick(self):
        """
        Кладёт ветку на клетку. Если это 3-я ветка — заменяется баррикадой.
        """
        if isinstance(self.object, Stick):
            if self.object.add_one():
                self.set_object(Barricade())
        elif self.object is None:
            self.set_object(Stick())

    def __repr__(self):
        return f"<Tile type={self.type} opaque={self.opaque} obj={self.object}>"
