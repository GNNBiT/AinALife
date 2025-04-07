import numpy as np
import torch

from core.tile_types import TileType
from core.world import Tile
from utils.direction import Direction


class PerceptionEncoder:
    TILE_CHANNELS = {
        TileType.EMPTY: 0,
        TileType.FOOD: 1,
        TileType.STONE: 2,
        TileType.COLONY: 3,
    }

    @staticmethod
    def encode_vision_as_cnn(world, ant):
        # создаем 4 канала 3x3 (или 5x5, если захочешь)
        channels = np.zeros((4, 3, 3), dtype=np.float32)

        dx, dy = ant.direction.to_vector()
        cx, cy = ant.x + dx, ant.y + dy

        for oy in [-1, 0, 1]:
            for ox in [-1, 0, 1]:
                tx = cx + ox
                ty = cy + oy
                tile = world.get_tile(tx, ty) or Tile(TileType.STONE)
                ch = PerceptionEncoder.TILE_CHANNELS[tile.type]
                channels[ch, oy + 1, ox + 1] = 1.0

        return channels

    @staticmethod
    def encode_tile(tile):
        one_hot = [0, 0, 0, 0]  # [empty, food, stone, colony]
        one_hot[tile.type.value] = 1
        return one_hot

    @staticmethod
    def encode_direction(direction):
        index = Direction.all().index(direction)  # <== индекс по позиции в списке
        one_hot = [0] * 8
        one_hot[index] = 1
        return one_hot

    @staticmethod
    def encode_ant_state(ant, tile):
        return [
            int(ant.carrying_food),
            int(tile.type == TileType.COLONY)
        ]


    @staticmethod
    def get_vision_tiles(world, ant):
        result = []

        # сначала тайл под собой
        tile_under = world.get_tile(ant.x, ant.y)
        result.append(tile_under)

        # теперь 3x3 перед муравьем
        dx, dy = ant.direction.to_vector()  # направление взгляда
        center_x = ant.x + dx
        center_y = ant.y + dy

        for oy in [-1, 0, 1]:
            for ox in [-1, 0, 1]:
                tx = center_x + ox
                ty = center_y + oy
                tile = world.get_tile(tx, ty)
                if tile:
                    result.append(tile)
                else:
                    result.append(Tile(TileType.STONE))  # или "заглушка"

        return result

    @staticmethod
    def encode_vision_as_cnn(world, ant):
        tiles = PerceptionEncoder.get_vision_tiles(world, ant)
        channels = 4  # colony, food, stone, empty
        vision_tensor = torch.zeros((channels, 3, 3), dtype=torch.float32)

        for idx, tile in enumerate(tiles[1:]):  # первые 9 — зрение
            x = idx % 3
            y = idx // 3
            if tile.type == TileType.COLONY:
                vision_tensor[0, y, x] = 1.0
            elif tile.contains_food:
                vision_tensor[1, y, x] = 1.0
            elif tile.type == TileType.STONE:
                vision_tensor[2, y, x] = 1.0
            else:
                vision_tensor[3, y, x] = 1.0

        return vision_tensor
