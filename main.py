from core.map_generator import load_config, generate_map
from core.agent import Ant
from simulation.simulator import Simulation
from visual.render_map import render_map

if __name__ == "__main__":
    config = load_config()
    world, colony_centers = generate_map(config)

    cx, cy = colony_centers[0]  # первый муравейник
    ants = [Ant(cx, cy, colony_centers[0])]

    sim = Simulation(world, ants)

    for _ in range(100):
        sim.step()

    render_map(world, config, ants)
