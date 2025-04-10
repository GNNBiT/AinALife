# world/render/pygame_render.py

import pygame
from world.config import (
    TILE_SIZE, TILE_TYPES, TILE_COLORS,
    COLOR_BG, COLOR_AGENT, COLOR_OBJECT_FOOD, COLOR_TEXT
)


def init_display(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("AntSim")
    return screen

def render_world(screen, world_map, ants, ui_state):
    screen.fill((0, 0, 0))  # фон

    # Рисуем тайлы
    for y in range(world_map.height):
        for x in range(world_map.width):
            tile = world_map.get_tile(x, y)
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            color = TILE_COLORS.get(tile.type, (30, 30, 30))  # по умолчанию — серый
            pygame.draw.rect(screen, color, rect)

            if tile.object:
                pygame.draw.circle(screen, COLOR_OBJECT_FOOD, rect.center, TILE_SIZE // 4)

    # Рисуем агентов
    for ant in ants:
        pos = (ant.x * TILE_SIZE + TILE_SIZE // 2, ant.y * TILE_SIZE + TILE_SIZE // 2)
        pygame.draw.circle(screen, COLOR_AGENT, pos, TILE_SIZE // 3)

    # UI
    draw_text(screen, f"Tick: {ui_state.tick}", (5, 5), color=COLOR_TEXT)
    draw_text(screen, f"Generation: {ui_state.generation}", (5, 25), color=COLOR_TEXT)
    draw_text(screen, f"Agents: {ui_state.ant_count}", (5, 45), color=COLOR_TEXT)

    pygame.display.flip()

def draw_text(surface, text, pos, color=(255, 255, 255), size=18):
    font = pygame.font.SysFont("Arial", size)
    render = font.render(text, True, color)
    surface.blit(render, pos)
