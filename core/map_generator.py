import numpy as np
import yaml
import random
from core.tile_types import TileType
from core.world import World

def load_config(path="configs/map_config.yaml"):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def generate_map(config, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    width = config['map']['width']
    height = config['map']['height']
    food_count = int(width * height * config['map']['food_percent'])
    stone_count = int(width * height * config['map']['stone_percent'])
    colony_count = config['map']['colony_count']
    colony_size = config['map'].get('colony_size', 3)

    world = World(width, height)
    colony_centers = []

    def place_random(tile_type, count):
        placed = 0
        while placed < count:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if world.get_tile(x, y).type == TileType.EMPTY:
                world.set_tile(x, y, tile_type)
                placed += 1

    def place_colonies(tile_type, count, size):
        placed = 0
        half = size // 2
        attempts = 0

        while placed < count and attempts < 1000:
            attempts += 1
            cx = random.randint(half, width - half - 1)
            cy = random.randint(half, height - half - 1)

            can_place = True
            for dx in range(-half, half + 1):
                for dy in range(-half, half + 1):
                    if world.get_tile(cx + dx, cy + dy).type != TileType.EMPTY:
                        can_place = False
                        break
                if not can_place:
                    break

            if can_place:
                for dx in range(-half, half + 1):
                    for dy in range(-half, half + 1):
                        world.set_tile(cx + dx, cy + dy, tile_type)

                # внутри if can_place:
                center = (cx, cy)
                colony_centers.append(center)

                placed += 1

    place_colonies(TileType.COLONY, colony_count, colony_size)
    place_random(TileType.FOOD, food_count)
    place_random(TileType.STONE, stone_count)

    return world, colony_centers
