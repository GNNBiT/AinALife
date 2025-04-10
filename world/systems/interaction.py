# world/systems/interaction.py

from world.entities.object import Food, Stick
from world.config import ENERGY_GAIN_IF_EAT_IN_NEST, ENERGY_GAIN_IF_EAT_OUTSIDE

def interact(agent, world_map, colony, action: str = "nothing"):
    tile = world_map.get_tile(agent.x, agent.y)
    obj = tile.object

    if action == "eat" and isinstance(obj, Food):
        if colony and is_in_nest(agent, colony):
            agent.energy += ENERGY_GAIN_IF_EAT_IN_NEST
        else:
            agent.energy += ENERGY_GAIN_IF_EAT_OUTSIDE
        agent.hunger = 0
        tile.remove_object()

    elif action == "pickup" and agent.status["carrying"] is None:
        if isinstance(obj, (Food, Stick)):
            agent.status["carrying"] = obj
            tile.remove_object()

    elif action == "drop" and agent.status["carrying"]:
        if tile.object is None:
            tile.set_object(agent.status["carrying"])
            agent.status["carrying"] = None

    # "nothing" или неизвестное действие — ничего не делаем

def is_in_nest(agent, colony):
    """Проверяет, стоит ли агент внутри своей базы 3x3"""
    nx, ny = colony.nest_center
    return abs(agent.x - nx) <= 1 and abs(agent.y - ny) <= 1
