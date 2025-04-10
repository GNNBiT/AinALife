# world/systems/reproduction.py

import random
from world.entities.ant import Ant

def reproduce(colonies, world_map, num_offspring_per_colony=5):
    """Создаёт новое поколение агентов по 5 штук на колонию."""

    new_ant = []

    for colony in colonies:
        cx, cy = colony.nest_center

        for _ in range(num_offspring_per_colony):
            # Немного рандомное смещение, чтобы не класть всех в одну точку
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            x, y = cx + dx, cy + dy

            ant = Ant(x=x, y=y)
            ant.facing = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            colony.register_agent(ant)
            new_ant.append(ant)

    return new_ant
