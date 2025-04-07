
import random

from core.tile_types import TileType
from models.ant_brain import AntBrain
from models.encoder import PerceptionEncoder
from models.info_packet import InfoPacket
from utils import ant_actions
from utils.direction import Direction

class Ant:
    def __init__(self, x, y, home_colony, energy=100, max_steps=200):
        self.x = x
        self.y = y
        self.colony_coords = home_colony
        self.energy = energy
        self.max_steps = max_steps
        self.steps = 0
        self.carrying_food = False
        self.direction = random.choice(Direction.all())  # смотрит в случайную сторону
        self.brain = AntBrain()
        self.spin_streak = 0

        self.target_food = None
        self.last_food_dist = None

    def is_alive(self):
        return self.steps < self.max_steps and self.energy > 0

    def act(self, world, ants, epsilon=0.0):
        inputs = self.get_inputs(world, ants)
        decision = self.brain.think(inputs, epsilon=epsilon)  # ⬅️ сюда
        self.steps += 1
        return ant_actions.act(self, world, ants, decision), inputs, decision

    def get_inputs(self, world, ants):
        inputs = {}

        vision_tensor = PerceptionEncoder.encode_vision_as_cnn(world, self)
        inputs["vision"] = vision_tensor  # [C, H, W]


        # Направление (one-hot)
        inputs["direction"] = PerceptionEncoder.encode_direction(self.direction)

        # Состояние (несёт еду, в муравейнике)
        tile_under = world.get_tile(self.x, self.y)
        inputs["flags"] = PerceptionEncoder.encode_ant_state(self, tile_under)
        inputs["tile_under"] = PerceptionEncoder.encode_tile(tile_under)  # ← ВОТ ЭТО ДОБАВЛЯЕМ

        # Координаты
        inputs["coords"] = [self.x, self.y]  # позже можно нормализовать, или заменить на относительные
        inputs["colony"] = list(self.colony_coords)

        # Память (заглушка — потом подключим реальную из AntBrain)
        if hasattr(self, "brain"):
            inputs["memory"] = self.brain.get_memory_vector()
        else:
            inputs["memory"] = []
        inputs["nearby_ants"] = self.get_ant_map(ants, radius=2)

        return inputs

    def get_ant_map(self, ants, radius=2):
        size = radius * 2 + 1
        grid = [[0 for _ in range(size)] for _ in range(size)]

        for other in ants:
            if other is self or not other.is_alive():
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            if abs(dx) <= radius and abs(dy) <= radius:
                gx = dx + radius
                gy = dy + radius
                grid[gy][gx] = 1

        # flatten grid → row-major 1D array
        flat = [cell for row in grid for cell in row]
        return flat  # 25 values: 0 или 1

