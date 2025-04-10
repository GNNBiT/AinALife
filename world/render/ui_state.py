# world/render/ui_state.py

class UIState:
    def __init__(self):
        self.tick = 0
        self.generation = 0
        self.agent_count = 0

    def update(self, world_manager):
        self.tick = world_manager.tick_count
        self.generation = world_manager.generation
        self.agent_count = len(world_manager.agents)
