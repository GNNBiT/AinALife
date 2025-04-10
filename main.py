# main.py

import pygame
from world.world_manager import WorldManager
from world.render.controls import get_controls_state
from world.render.ui_state import UIState
from world.render.pygame_render import init_display, render_world
from world.config import TILE_SIZE

def main():
    # Инициализация мира
    manager = WorldManager(colony_count=2)
    ui_state = UIState()

    # Окно pygame
    screen_width = manager.world_map.width * TILE_SIZE
    screen_height = manager.world_map.height * TILE_SIZE
    screen = init_display(screen_width, screen_height)

    clock = pygame.time.Clock()
    paused = False

    running = True
    while running:
        controls = get_controls_state()
        if controls["quit"]:
            running = False

        if controls["step"]:
            manager.step()

        if not paused and not controls["step"]:
            manager.step()

        paused = controls["paused"]

        ui_state.update(manager)
        render_world(screen, manager.world_map, manager.ants, ui_state)

        clock.tick(10)  # FPS

    pygame.quit()

if __name__ == "__main__":
    main()
