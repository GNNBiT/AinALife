import numpy as np

from input_data import InputData
from world.config import TILE_TYPES, DIRECTION_LIST
import random

import torch
import torch.nn as nn
import torch.nn.functional as F

from world.systems.perception import get_cone_vision, get_scent


class AntBrain(nn.Module):
    def __init__(self):
        super().__init__()

        # CNN часть для восприятия окружающей среды
        self.tile_cnn = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Flatten()
        )

        self.pheromone_cnn = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(8, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Flatten()
        )

        # LSTM часть для временных союзников или других последовательностей
        self.ally_lstm = nn.LSTM(input_size=5, hidden_size=32, batch_first=True)

        # LSTM для пути (последние 30 клеток)
        self.path_lstm = nn.LSTM(input_size=4, hidden_size=32, batch_first=True)

        # MLP часть для скалярных признаков
        self.scalar_mlp = nn.Sequential(
            nn.Linear(6, 32),  # например: x, y, direction, energy, hunger, age
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU()
        )

        # Финальный блок объединения
        self.final = nn.Sequential(
            nn.Linear(32*2 + 16*8*8 + 64, 128),  # учти размер после Flatten у CNN
            nn.ReLU(),
            nn.Linear(128, 8)  # например, 8 возможных действий
        )

        # Только одна "голова" — действия
        self.action_head = nn.Linear(128, 7)

    def forward(self, tiles, pheromones, allies, scalars, path_history):
        # tiles, pheromones: [B, 1, H, W]
        # allies: [B, N, D] — N союзников, D признаков
        # scalars: [B, S] — S скалярных признаков
        # path_history: [B, 30, 3] — x, y, direction_idx

        tile_out = self.tile_cnn(tiles)  # [B, CNN_flat_dim]
        pheromone_out = self.pheromone_cnn(pheromones)

        # Allies (если не через LSTM)
        ally_flat = allies.view(allies.size(0), -1)  # [B, N*D]
        ally_out = self.ally_mlp(ally_flat)

        scalar_out = self.scalar_mlp(scalars)

        # Path LSTM
        _, (path_lstm_out, _) = self.path_lstm(path_history)
        path_out = path_lstm_out[-1]  # [B, 32]

        # Собираем всё вместе
        combined = torch.cat([tile_out, pheromone_out, ally_out, scalar_out, path_out], dim=1)
        shared = self.shared(combined)

        action_logits = self.action_head(shared)
        return {"action": action_logits}

    def gather_input_data(self, ant, world, allies):
        input_data = {}
        visible_coords = set(get_cone_vision(ant, world))

        # --- 1. Зрение: список видимых координат ---
        input_data["visible_tiles"] = visible_coords

        # --- 2. Запах ---
        input_data["pheromones_around"] = get_scent(ant, world)  # Dict[(x, y)] = scent_data

        # --- 3. Союзники ---
        visible_allies = [ally for ally in allies if (ally.x, ally.y) in visible_coords]

        input_data["allies"] = [ally.get_features() for ally in visible_allies]

        # --- 4. Скаляры ---
        input_data["scalars"] = np.array([
            ant.x,
            ant.y,
            DIRECTION_LIST.index(ant.facing),
            ant.energy,
            ant.hunger,
            ant.health
        ], dtype=np.float32)

        # --- 5. Путь ---
        path = list(ant.path_memory)
        path_len = len(path)

        if path_len < 30:
            pad = [(0.0, 0.0, -1.0, 0.0)] * (30 - path_len)
            path = pad + [(x, y, dir_idx, 1.0) for (x, y, dir_idx) in path]
        else:
            # если уже храним (x, y, dir_idx, valid), то просто передаём
            pass

        input_data["path_history"] = np.array(path, dtype=np.float32)

        return input_data
