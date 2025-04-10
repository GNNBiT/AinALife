# world/systems/movement.py

from world.config import DIRECTIONS

def update(ant, world_map):
    """Обновляет позицию агента, если движение возможно"""

    dx, dy = ant.facing  # текущее направление взгляда

    new_x = ant.x + dx
    new_y = ant.y + dy

    # Проверка границ и проходимости
    if not world_map.in_bounds(new_x, new_y):
        return False

    if not world_map.is_walkable(new_x, new_y):
        return False

    # Движение
    ant.set_position(new_x, new_y)

    # Можно позже: уменьшить энергию, голод и т.д.
    ant.energy -= 1
    ant.hunger += 1

    return True
