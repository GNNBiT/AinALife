# world/systems/movement.py

from world.config import DIRECTIONS

def update(agent, world_map):
    """Обновляет позицию агента, если движение возможно"""

    dx, dy = agent.facing  # текущее направление взгляда

    new_x = agent.x + dx
    new_y = agent.y + dy

    # Проверка границ и проходимости
    if not world_map.in_bounds(new_x, new_y):
        return False

    if not world_map.is_walkable(new_x, new_y):
        return False

    # Движение
    agent.set_position(new_x, new_y)

    # Можно позже: уменьшить энергию, голод и т.д.
    agent.energy -= 1
    agent.hunger += 1

    return True
