# world/systems/perception.py

from world.config import DIRECTION_LIST
from math import copysign

def get_cone_vision(agent, world_map):
    """3x3 зона перед агентом, с raycast-проверкой на видимость"""
    visible = set()
    cx, cy = agent.x, agent.y
    dx, dy = agent.facing
    r = agent.vision_range  # радиус (длина конуса)

    zone = get_cone_zone(cx, cy, dx, dy, r)

    for tx, ty in zone:
        if not world_map.in_bounds(tx, ty):
            continue

        if is_visible(cx, cy, tx, ty, world_map):
            visible.add((tx, ty))

    return list(visible)

def get_cone_zone(cx, cy, dx, dy, length):
    offsets = []

    if dx != 0 and dy == 0:  # горизонталь
        for i in range(1, length + 1):
            for j in [-1, 0, 1]:
                offsets.append((cx + dx * i, cy + j))

    elif dy != 0 and dx == 0:  # вертикаль
        for i in range(1, length + 1):
            for j in [-1, 0, 1]:
                offsets.append((cx + j, cy + dy * i))

    else:  # диагонали
        for i in range(1, length + 1):
            for j in [-1, 0, 1]:
                offsets.append((cx + dx * i + j * dy, cy + dy * i + j * dx))

    return offsets

def is_visible(x0, y0, x1, y1, world_map):
    """Проверяет, можно ли видеть из (x0, y0) в (x1, y1) — line of sight"""
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return True

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x0 + 0.5, y0 + 0.5
    for _ in range(steps):
        x += x_inc
        y += y_inc
        tx, ty = int(x), int(y)
        if not world_map.in_bounds(tx, ty):
            return False
        if (tx, ty) == (x1, y1):
            break
        tile = world_map.get_tile(tx, ty)
        if tile.opaque:
            return False
    return True

def get_scent(agent, world_map):
    """Возвращает запахи вокруг агента в радиусе scent_radius"""
    scents = {}

    radius = agent.scent_radius
    cx, cy = agent.x, agent.y

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            x = cx + dx
            y = cy + dy

            if not world_map.in_bounds(x, y):
                continue

            scent_data = world_map.get_scent(x, y)
            if scent_data:
                scents[(x, y)] = scent_data.copy()

    return scents
