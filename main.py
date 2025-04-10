# main.py

from world.world_manager import WorldManager
from world.entities.agent import Agent
from world.systems import movement
from world.systems.perception import get_cone_vision
from world.config import TILE_TYPES

def print_map_with_vision(world_map, agent, visible_tiles):
    for y in range(world_map.height):
        row = ""
        for x in range(world_map.width):
            if (x, y) == (agent.x, agent.y):
                row += "A"
            elif (x, y) in visible_tiles:
                row += "*"
            else:
                tile = world_map.get_tile(x, y)
                if tile.type == TILE_TYPES["ROCK"]:
                    row += "#"
                else:
                    row += "."
        print(row)

def main():
    # Создаём мир с 2 колониями
    manager = WorldManager(colony_count=2)

    # Размещаем агента вручную
    agent = Agent(x=10, y=10)
    agent.facing = (0, 1)

    # Показываем начальное состояние
    print("=== INITIAL STATE ===")
    print(f"Tick: {manager.tick_count}")
    print(f"Nests: {manager.nest_positions}")
    print(f"Conditions: {manager.conditions}")

    for colony in manager.colonies:
        print(colony)

    # Делаем 5 шагов симуляции
    for _ in range(5):
        manager.step()
        print(f"Tick: {manager.tick_count}")

    # === ТЕСТ ЗРЕНИЯ ===
    print("\n=== ПОЛЕ ЗРЕНИЯ АГЕНТА ===")
    visible = get_cone_vision(agent, manager.world_map)
    print_map_with_vision(manager.world_map, agent, set(visible))

if __name__ == "__main__":
    main()
