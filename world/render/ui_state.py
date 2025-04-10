# world/render/ui_state.py

class UIState:
    def __init__(self):
        self.tick = 0
        self.generation = 0
        self.ant_count = 0

    def update(self, world_manager):
        self.tick = world_manager.tick_count
        self.generation = world_manager.generation
        self.ant_count = len(world_manager.ants)
