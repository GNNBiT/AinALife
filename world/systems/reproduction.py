# world/systems/reproduction.py

import random
from world.entities.agent import Agent

def reproduce(colonies, world_map, num_offspring_per_colony=5):
    """Создаёт новое поколение агентов по 5 штук на колонию."""

    new_agents = []

    for colony in colonies:
        cx, cy = colony.nest_center

        for _ in range(num_offspring_per_colony):
            # Немного рандомное смещение, чтобы не класть всех в одну точку
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            x, y = cx + dx, cy + dy

            agent = Agent(x=x, y=y)
            agent.facing = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            colony.register_agent(agent)
            new_agents.append(agent)

    return new_agents
