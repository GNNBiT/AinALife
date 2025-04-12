class InputData:
    def __init__(
        self,
        position,           # (x, y)
        facing,             # (dx, dy)
        energy,             # float
        hunger,             # float
        health,             # float
        carrying,           # str | None

        nest_position,      # (x, y)
        colony_id,          # int
        colony_relations,   # dict[colony_id -> trust]

        vision_tiles,       # list of dicts: {dx, dy, tile_type, object_type, ant_info?}
        visible_allies,     # list of dicts: {id, dx, dy, respect}

        scent_map,          # list of dicts: {dx, dy, scents: list[{"type", "colony_id", "intensity"}]}
    ):
        self.position = position
        self.facing = facing
        self.energy = energy
        self.hunger = hunger
        self.health = health
        self.carrying = carrying

        self.nest_position = nest_position
        self.colony_id = colony_id
        self.colony_relations = colony_relations

        self.vision_tiles = vision_tiles
        self.visible_allies = visible_allies

        self.scent_map = scent_map
