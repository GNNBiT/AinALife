class Simulation:
    def __init__(self, world, agents):
        self.world = world
        self.agents = agents
        self.tick = 0

    def step(self):
        for agent in self.agents:
            if agent.is_alive():
                agent.act(self.world, self.agents)
        self.tick += 1
