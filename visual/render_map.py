import pygame
from core.tile_types import TileType

TILE_SIZE = 16  # Размер одного тайла

def render_map(world, config, ants=None):
    width, height = world.width, world.height
    screen_size = (width * TILE_SIZE, height * TILE_SIZE)

    # Цвета тайлов из конфигурации
    color_config = config.get('colors', {})
    tile_colors = {
        TileType.EMPTY: pygame.Color(color_config.get('EMPTY', '#000000')),
        TileType.FOOD: pygame.Color(color_config.get('FOOD', '#00ff00')),
        TileType.STONE: pygame.Color(color_config.get('STONE', '#808080')),
        TileType.COLONY: pygame.Color(color_config.get('COLONY', '#ffff00')),
    }

    ant_color = pygame.Color(color_config.get('Ant', '#ff0000'))

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Ant World — Pygame View")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for y in range(height):
            for x in range(width):
                tile = world.get_tile(x, y)
                color = tile_colors.get(tile.type, pygame.Color('black'))
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, color, rect)

        # Отрисовка агентов
        if ants:
            for ant in ants:
                if ant.is_alive():
                    px = ant.x * TILE_SIZE + TILE_SIZE // 2
                    py = ant.y * TILE_SIZE + TILE_SIZE // 2
                    radius = TILE_SIZE // 3
                    pygame.draw.circle(screen, ant_color, (px, py), radius)

        pygame.display.flip()

    pygame.quit()
    
