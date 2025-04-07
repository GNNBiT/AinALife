from math import dist, atan2, pi

from models.info_packet import InfoPacket
from core.tile_types import TileType
from models.encoder import PerceptionEncoder

def act(ant, world, ants, decision):
    action = decision["action"]
    perceive_and_share_food(ant, world, ants)
    maybe_share_carrying_status(ant, ants)

    match action:
        case "MOVE_FORWARD":
            ant.spin_streak = 0
            result = move_forward(ant, world)
        case "MOVE_BACKWARD":
            ant.spin_streak = 0
            result = move_backward(ant, world)
        case "PICK_FOOD":
            ant.spin_streak = 0
            result = pick_food(ant, world, ants)
        case "DROP_FOOD":
            ant.spin_streak = 0
            result = drop_food(ant, world)
        case "TURN_LEFT":
            result = turn_left(ant)
        case "TURN_RIGHT":
            result = turn_right(ant)
        case _:
            result = 0.0

    #result += evaluate_food_seek_reward(ant, world)
    return result


def perceive_and_share_food(ant, world, ants):
    vision = PerceptionEncoder.get_vision_tiles(world, ant)
    for i, tile in enumerate(vision):
        if tile.type == TileType.FOOD:
            coords = vision_index_to_coords(ant, i)
            if not food_known(ant, coords):
                packet = InfoPacket("food", coords)
                ant.brain.receive(packet)
                broadcast(ant, ants, packet)

            if not ant.carrying_food and ant.target_food is None:
                ant.target_food = coords
                ant.last_food_dist = dist((ant.x, ant.y), coords)


def move_forward(ant, world):
    dx, dy = ant.direction.to_vector()
    return attempt_move(ant, world, ant.x + dx, ant.y + dy)

def move_backward(ant, world):
    dx, dy = ant.direction.to_vector()
    return attempt_move(ant, world, ant.x - dx, ant.y - dy)


def attempt_move(ant, world, new_x, new_y):
    success, reward = world.move_ant(ant.x, ant.y, new_x, new_y)
    ant.energy -= 0.1

    if success:
        old_dist = dist((ant.x, ant.y), ant.colony_coords)
        new_dist = dist((new_x, new_y), ant.colony_coords)

        # Обновляем координаты
        ant.x, ant.y = new_x, new_y

        # Если муравей несет еду и движется ближе к базе
        if ant.carrying_food:
            if new_dist < old_dist:
                reward += 0.4  # маленькая награда
            else:
                ant.energy -= 0.2
                reward -= 0.2  # небольшой штраф, чтобы не шатался

    return reward

def turn_left(ant):
    old_dir = ant.direction
    new_dir = ant.direction.turn_left()

    ant.spin_streak += 1
    if ant.spin_streak > 6:
        ant.energy -= 0.5
        return -0.5  # 👈 штраф за крутёжку

    ant.energy -= 0.01
    reward = -0.01  # базовый штраф

    if ant.carrying_food:
        reward += angle_reward(old_dir, new_dir, ant, target=ant.colony_coords)

    ant.direction = new_dir
    return reward

def turn_right(ant):
    old_dir = ant.direction
    new_dir = ant.direction.turn_right()

    ant.spin_streak += 1
    if ant.spin_streak > 6:
        ant.energy -= 0.5
        return -0.5  # 👈 штраф за крутёжку

    ant.energy -= 0.01
    reward = -0.01

    if ant.carrying_food:
        reward += angle_reward(old_dir, new_dir, ant, target=ant.colony_coords)

    ant.direction = new_dir
    return reward


def pick_food(ant, world, ants):
    if ant.carrying_food:
        ant.energy -= 0.2
        return -0.2  # штраф за попытку взять еду, когда уже несёшь

    tile = world.get_tile(ant.x, ant.y)
    success, reward = tile.pick_food()
    ant.energy -= reward if reward < 0 else 0
    if success:
        print(f"[EVENT] Picked food at ({ant.x}, {ant.y})")
        ant.carrying_food = True
        packet = InfoPacket("food_gone", (ant.x, ant.y))
        ant.brain.receive(packet)
        broadcast(ant, ants, packet)
    return reward


def drop_food(ant, world):
    if not ant.carrying_food:
        ant.energy -= 0.2
        return -0.2  # 👈 штраф за попытку сдать еду без еды

    tile = world.get_tile(ant.x, ant.y)
    success, reward = tile.drop_food()
    ant.energy -= reward if reward < 0 else 0
    if success:
        print(f"[EVENT] Dropped food at ({ant.x}, {ant.y})")
        ant.carrying_food = False
    return reward


def broadcast(sender, ants, packet, radius=2):
    for other in ants:
        if other is sender or not other.is_alive():
            continue
        dx = abs(sender.x - other.x)
        dy = abs(sender.y - other.y)
        if dx <= radius and dy <= radius:
            other.brain.receive(packet)

def food_known(ant, coords):
    return any(p.type == "food" and p.data == coords for p in ant.brain.memory)

def vision_index_to_coords(ant, index):
    dx, dy = ant.direction.to_vector()
    cx, cy = ant.x + dx, ant.y + dy
    offsets = [(-1,-1), (0,-1), (1,-1), (-1,0), (0,0), (1,0), (-1,1), (0,1), (1,1)]
    if index == 0:
        return (ant.x, ant.y)
    ox, oy = offsets[index - 1]
    return (cx + ox, cy + oy)

def maybe_share_carrying_status(ant, ants):
    if ant.carrying_food:
        packet = InfoPacket("carrying_food", (ant.x, ant.y))
        ant.brain.receive(packet)
        broadcast(ant, ants, packet)

def angle_reward(old_dir, new_dir, ant, target):
    def dir_to_angle(direction):
        dx, dy = direction.to_vector()
        return atan2(dy, dx)

    def vector_to_angle(dx, dy):
        return atan2(dy, dx)

    # Угол на базу
    tx, ty = target
    vec_to_base = (tx - ant.x, ty - ant.y)
    base_angle = vector_to_angle(*vec_to_base)

    # Направления
    old_angle = dir_to_angle(old_dir)
    new_angle = dir_to_angle(new_dir)

    def angle_diff(a1, a2):
        return min(abs(a1 - a2), 2 * pi - abs(a1 - a2))

    # Насколько улучшилось направление
    delta_before = angle_diff(old_angle, base_angle)
    delta_after = angle_diff(new_angle, base_angle)

    improvement = delta_before - delta_after

    # Награждаем, если стал ближе к направлению на базу
    return max(0.0, 0.1 * improvement)

def evaluate_food_seek_reward(ant, world):
    if ant.carrying_food or ant.target_food is None:
        return 0.0

    reward = 0.0
    current_dist = dist((ant.x, ant.y), ant.target_food)

    # Если муравей уже пришел к цели — сбрасываем цель (без штрафа)
    if (ant.x, ant.y) == ant.target_food:
        ant.target_food = None
        ant.last_food_dist = None
        return reward  # без бонуса и штрафа, он дошёл

    # Награда за приближение
    if ant.last_food_dist and current_dist < ant.last_food_dist:
        reward += 0.2
    elif ant.last_food_dist and current_dist > ant.last_food_dist + 0.5:
        ant.energy -= 0.3
        reward -= 0.3

    ant.last_food_dist = current_dist

    # Проверяем — видно ли цель в зрении
    vision = PerceptionEncoder.get_vision_tiles(world, ant)
    visible = any(
        vision_index_to_coords(ant, i) == ant.target_food and tile.type == TileType.FOOD
        for i, tile in enumerate(vision)
    )

    if not visible:
        ant.energy -= 5.0
        reward -= 5.0  # штраф за потерю из виду
        ant.target_food = None
        ant.last_food_dist = None

    return reward
