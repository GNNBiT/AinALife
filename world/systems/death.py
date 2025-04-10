# world/systems/death.py

from world.entities.object import Corpse
from world.config import HUNGER_DEATH_THRESHOLD

def check_death(ant, world_map, ants_list):
    """Проверяет, умер ли агент, и если да — удаляет и превращает в падаль"""

    if ant.energy <= 0 or ant.hunger >= HUNGER_DEATH_THRESHOLD:
        # Падаль на месте смерти
        tile = world_map.get_tile(ant.x, ant.y)
        if tile.object is None:
            tile.set_object(Corpse(size=1.0))  # можно брать вес из агента, если есть

        # Удаление из списка агентов
        if ant in ants_list:
            ants_list.remove(ant)

        return True

    return False
