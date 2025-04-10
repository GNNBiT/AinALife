# world/render/controls.py

import pygame

def get_controls_state():
    """
    Возвращает словарь состояния управления:
    paused, step, quit
    """
    controls = {
        "paused": False,
        "step": False,
        "quit": False
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            controls["quit"] = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                controls["quit"] = True
            elif event.key == pygame.K_SPACE:
                controls["paused"] = True
            elif event.key == pygame.K_s:
                controls["step"] = True

    return controls
