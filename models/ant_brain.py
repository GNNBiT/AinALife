from input_data import InputData
from world.config import TILE_TYPES
import random


class AntBrain:
    def __init__(self, genes=None):
        pass

    @staticmethod
    def gather_input_data(ant, world):
        x, y = ant.get_position()
        colony = next((c for c in world.colonies if c.nest_center == world.nest_positions[ant.colony_id]), None)

        # Визуальная зона
        vision_tiles = []
        visible_allies = []

        for dx in range(-ant.vision_range, ant.vision_range + 1):
            for dy in range(-ant.vision_range, ant.vision_range + 1):
                tx, ty = x + dx, y + dy
                if not world.world_map.in_bounds(tx, ty):
                    continue
                tile = world.world_map.get_tile(tx, ty)

                tile_type = tile.type
                object_type = next((obj.type for obj in tile.objects.values()), None)

                ant_info = None
                for other_ant in world.ants:
                    if other_ant.id != ant.id and other_ant.get_position() == (tx, ty):
                        ant_info = {"id": other_ant.id, "colony_id": other_ant.colony_id}
                        if other_ant.colony_id == ant.colony_id:
                            respect = ant.respect.get(other_ant.id, 0.0)
                            visible_allies.append({"id": other_ant.id, "dx": dx, "dy": dy, "respect": respect})
                        break

                vision_tiles.append({
                    "dx": dx,
                    "dy": dy,
                    "tile_type": tile_type,
                    "object_type": object_type,
                    "ant": ant_info
                })

        # Сбор запахов
        scent_map = []
        for dx in range(-ant.scent_radius, ant.scent_radius + 1):
            for dy in range(-ant.scent_radius, ant.scent_radius + 1):
                tx, ty = x + dx, y + dy
                if not world.world_map.in_bounds(tx, ty):
                    continue
                scents = world.world_map.scent_map.get_all(tx, ty)
                scent_map.append({"dx": dx, "dy": dy, "scents": scents})

        return InputData(
            position=(x, y),
            facing=ant.facing,
            energy=ant.energy,
            hunger=ant.hunger,
            health=ant.health,
            carrying=ant.status.get("carrying").type if ant.status.get("carrying") else None,

            nest_position=colony.nest_center if colony else None,
            colony_id=ant.colony_id,
            colony_relations=colony.relationships if colony else {},

            vision_tiles=vision_tiles,
            visible_allies=visible_allies,

            scent_map=scent_map
        )
