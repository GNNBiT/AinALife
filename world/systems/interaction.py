# world/systems/interaction.py

from world.entities.object import Food, Stick
from world.config import ENERGY_GAIN_IF_EAT_IN_NEST, ENERGY_GAIN_IF_EAT_OUTSIDE

def interact(ant, world_map, colony, action: str = "nothing"):
    tile = world_map.get_tile(ant.x, ant.y)
    obj = tile.object

    # === Поедание еды ===
    if action == "eat" and isinstance(obj, Food):
        reward = ENERGY_GAIN_IF_EAT_IN_NEST if is_in_nest(ant, colony) else ENERGY_GAIN_IF_EAT_OUTSIDE

        gained = obj.take_bite()
        ant.energy += min(gained, reward)
        ant.hunger = 0

        if obj.is_empty():
            tile.remove_object()

    elif action == "pickup" and ant.status["carrying"] is None:
        if isinstance(obj, Food):
            # забираем одну единицу еды
            new_item = obj.__class__()  # создаём копию того же типа (Berry / Corpse)
            new_item.amount = 1
            new_item.nutrition_per_unit = obj.nutrition_per_unit
            new_item.decay = obj.decay  # можно копировать decay

            ant.status["carrying"] = new_item
            obj.amount -= 1

            if obj.is_empty():
                tile.remove_object()

        elif isinstance(obj, Stick):
            ant.status["carrying"] = obj
            tile.remove_object()


    # === Бросить предмет ===
    elif action == "drop" and ant.status["carrying"]:
        item = ant.status["carrying"]

        if isinstance(item, Stick):
            tile.place_stick()
        elif tile.object is None:
            tile.set_object(item)

        ant.status["carrying"] = None

    # === "nothing" — ничего не делаем

def is_in_nest(ant, colony):
    """Проверяет, стоит ли агент внутри своей базы 3x3"""
    nx, ny = colony.nest_center
    return abs(ant.x - nx) <= 1 and abs(ant.y - ny) <= 1
