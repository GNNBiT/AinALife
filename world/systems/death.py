# world/systems/death.py

from world.entities.object import Corpse
from world.config import HUNGER_DEATH_THRESHOLD

def check_death(agent, world_map, agents_list):
    """Проверяет, умер ли агент, и если да — удаляет и превращает в падаль"""

    if agent.energy <= 0 or agent.hunger >= HUNGER_DEATH_THRESHOLD:
        # Падаль на месте смерти
        tile = world_map.get_tile(agent.x, agent.y)
        if tile.object is None:
            tile.set_object(Corpse(size=1.0))  # можно брать вес из агента, если есть

        # Удаление из списка агентов
        if agent in agents_list:
            agents_list.remove(agent)

        return True

    return False
