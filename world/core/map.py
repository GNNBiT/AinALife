# world/core/map.py

from world.core.tile import Tile
from world.config import MAP_WIDTH, MAP_HEIGHT, TILE_TYPES

class WorldMap:
    def __init__(self, width=MAP_WIDTH, height=MAP_HEIGHT):
        self.width = width
        self.height = height
        self.grid = [
            [Tile(TILE_TYPES["GROUND"]) for _ in range(width)]
            for _ in range(height)
        ]
        self.scent_map = [[{} for _ in range(width)] for _ in range(height)]

    def in_bounds(self, x: int, y: int) -> bool:
        """Проверка, что координаты в пределах карты"""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tile(self, x: int, y: int) -> Tile:
        """Возвращает тайл по координатам"""
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]  # [строки][столбцы]

    def set_tile(self, x: int, y: int, tile: Tile):
        """Устанавливает тайл в координаты"""
        if self.in_bounds(x, y):
            self.grid[y][x] = tile

    def is_walkable(self, x: int, y: int) -> bool:
        """Можно ли пройти на эту клетку"""
        tile = self.get_tile(x, y)
        return tile is not None and tile.can_enter()

    def place_object(self, x: int, y: int, obj):
        """Размещает объект (еда, ветка, падаль) на тайле"""
        tile = self.get_tile(x, y)
        if tile and tile.is_empty():
            tile.set_object(obj)
            return True
        return False

    def remove_object(self, x: int, y: int):
        """Удаляет объект с тайла"""
        tile = self.get_tile(x, y)
        if tile:
            tile.remove_object()

    def __repr__(self):
        return f"<WorldMap {self.width}x{self.height}>"
