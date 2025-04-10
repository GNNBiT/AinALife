# world/systems/interaction.py

from world.entities.object import Food, Stick
from world.config import ENERGY_GAIN_IF_EAT_IN_NEST, ENERGY_GAIN_IF_EAT_OUTSIDE

def interact(ant, world_map, colony, action: str = "nothing"):
    tile = world_map.get_tile(ant.x, ant.y)
    obj = tile.object

    if action == "eat" and isinstance(obj, Food):
        if colony and is_in_nest(ant, colony):
            ant.energy += ENERGY_GAIN_IF_EAT_IN_NEST
        else:
            ant.energy += ENERGY_GAIN_IF_EAT_OUTSIDE
        ant.hunger = 0
        tile.remove_object()

    elif action == "pickup" and ant.status["carrying"] is None:
        if isinstance(obj, (Food, Stick)):
            ant.status["carrying"] = obj
            tile.remove_object()

    elif action == "drop" and ant.status["carrying"]:
        if tile.object is None:
            tile.set_object(ant.status["carrying"])
            ant.status["carrying"] = None

    # "nothing" или неизвестное действие — ничего не делаем

def is_in_nest(ant, colony):
    """Проверяет, стоит ли агент внутри своей базы 3x3"""
    nx, ny = colony.nest_center
    return abs(ant.x - nx) <= 1 and abs(ant.y - ny) <= 1
