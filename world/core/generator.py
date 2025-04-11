# world/core/generator.py

import random
from world.core.map import WorldMap
from world.core.tile import Tile
from world.config import (
    TILE_TYPES,
    OBSTACLE_DENSITY,
    FOOD_DENSITY,
    DEFAULT_SEED
)
from world.entities.object import Berry


def generate_map(width, height, colony_count=1, seed=DEFAULT_SEED):
    random.seed(seed)
    world_map = WorldMap(width, height)

    nests = place_nests(world_map, colony_count)
    place_obstacles(world_map)
    place_food(world_map)

    return world_map, nests

def place_obstacles(world_map):
    for y in range(world_map.height):
        for x in range(world_map.width):
            tile = world_map.get_tile(x, y)
            if tile.type != TILE_TYPES["GROUND"]:
                continue  # НЕ ставим поверх NEST или других типов
            if random.random() < OBSTACLE_DENSITY:
                world_map.set_tile(x, y, Tile(TILE_TYPES["ROCK"]))

def place_food(world_map):
    total = int(world_map.width * world_map.height * FOOD_DENSITY)
    for _ in range(total):
        x = random.randint(0, world_map.width - 1)
        y = random.randint(0, world_map.height - 1)
        tile = world_map.get_tile(x, y)
        if tile and tile.type == TILE_TYPES["GROUND"] and tile.is_empty():
            berry = Berry()
            tile.set_object(berry)
            world_map.scent_map.emit(
                x, y,
                scent_type="food",
                colony_id=-1,  # от мира
                intensity=5,
                radius=6,
                lifespan=berry.decay,
                direction=None
            )

def place_nests(world_map, colony_count):
    nests = []
    min_distance = world_map.width // max(colony_count * 2, 2)
    attempts = 0
    while len(nests) < colony_count and attempts < 1000:
        x = random.randint(1, world_map.width - 4)
        y = random.randint(1, world_map.height - 4)
        if is_area_clear(world_map, x, y, size=3, min_dist=min_distance, existing=nests):
            for dy in range(3):
                for dx in range(3):
                    world_map.set_tile(x + dx, y + dy, Tile(TILE_TYPES["NEST"]))
            nests.append((x + 1, y + 1))
        attempts += 1
    return nests

def is_area_clear(world_map, x, y, size=3, min_dist=10, existing=None):
    if existing is None:
        existing = []
    for dy in range(size):
        for dx in range(size):
            tx, ty = x + dx, y + dy
            if not world_map.in_bounds(tx, ty):
                return False
            tile = world_map.get_tile(tx, ty)
            if tile.type != TILE_TYPES["GROUND"]:
                return False
    for (nx, ny) in existing:
        if abs(nx - x) < min_dist and abs(ny - y) < min_dist:
            return False
    return True
