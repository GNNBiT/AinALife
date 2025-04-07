from core.tile_types import TileType

class Tile:
    def __init__(self, tile_type: TileType):
        self.type = tile_type
        self.contains_food = tile_type == TileType.FOOD
        self.is_solid = tile_type == TileType.STONE

    def is_walkable(self):
        return not self.is_solid

    def pick_food(self):
        if self.contains_food:
            self.contains_food = False
            self.type = TileType.EMPTY
            return True, +9  # награда за сбор еды
        return False, -0.1  # штраф за бесполезное действие

    def drop_food(self):
        if self.type == TileType.COLONY:
            return True, +30.0  # большая награда за доставку еды домой
        return False, -0.1


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Tile(TileType.EMPTY) for _ in range(width)] for _ in range(height)]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tile(self, x, y):
        if self.in_bounds(x, y):
            return self.grid[y][x]
        return None

    def set_tile(self, x, y, tile_type: TileType):
        if self.in_bounds(x, y):
            self.grid[y][x] = Tile(tile_type)

    def move_ant(self, from_x, from_y, to_x, to_y):
        if not self.in_bounds(to_x, to_y):
            return False, -4.0  # штраф за выход за границу

        target_tile = self.get_tile(to_x, to_y)

        if not target_tile.is_walkable():
            return False, -0.5  # штраф за попытку пройти сквозь препятствие

        return True, -0.01  # обычный шаг, с минимальной "ценой энергии"

    def is_occupied(self, x, y, ants):
        return any(ant.x == x and ant.y == y and ant.is_alive() for ant in ants)

