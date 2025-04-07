import torch
import torch.nn as nn
import torch.nn.functional as F

class AntNet(nn.Module):
    def __init__(self, input_dim=64, lstm_hidden=64, mlp_hidden=64, num_actions=6):
        super(AntNet, self).__init__()

        # ant_net.py — замени vision_proj на сверточный блок
        self.vision_proj = nn.Sequential(
            nn.Conv2d(4, 8, kernel_size=2),  # (4, 3, 3) → (8, 2, 2)
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.ReLU(),
            nn.Flatten()  # → (32,)
        )

        self.dir_proj = nn.Sequential(
            nn.Linear(8, 8),
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.ReLU()
        )
        self.flags_proj = nn.Sequential(
            nn.Linear(2, 4),
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.ReLU()
        )
        self.coords_proj = nn.Sequential(
            nn.Linear(2, 4),
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.ReLU()
        )

        self.colony_proj = nn.Sequential(
            nn.Linear(2, 4),
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.ReLU()
        )

        self.nearby_proj = nn.Sequential(
            nn.Linear(25, 8),
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.ReLU()
        )

        self.tile_proj = nn.Sequential(
            nn.Linear(4, 4),  # 4 one-hot признака
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.ReLU()
        )

        # LSTM
        self.lstm = nn.LSTM(input_dim, lstm_hidden, batch_first=True)

        # Actor и Critic
        self.actor = nn.Sequential(
            nn.Linear(lstm_hidden, mlp_hidden),
            nn.ReLU(),
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.Linear(mlp_hidden, num_actions)
        )

        self.critic = nn.Sequential(
            nn.Linear(lstm_hidden, mlp_hidden),
            nn.ReLU(),
            nn.Dropout(0.2),  # 👈 добавили dropout
            nn.Linear(mlp_hidden, 1)
        )

    def forward(self, inputs: dict, hidden_state=None):

        # Раздельная обработка
        # ant_net.py → forward
        vision = inputs["vision"].clone().detach().unsqueeze(0).float()
        direction = torch.tensor(inputs["direction"], dtype=torch.float32).unsqueeze(0)
        flags = torch.tensor(inputs["flags"], dtype=torch.float32).unsqueeze(0)
        coords = torch.tensor(inputs["coords"], dtype=torch.float32).unsqueeze(0)
        nearby = torch.tensor(inputs.get("nearby_ants", inputs.get("nearby", [0]*25)), dtype=torch.float32).unsqueeze(0)
        colony = torch.tensor(inputs["colony"], dtype=torch.float32).unsqueeze(0)
        tile_under = torch.tensor(inputs["tile_under"], dtype=torch.float32).unsqueeze(0)

        # Преобразование
        t = self.tile_proj(tile_under)  # 👈 добавим этот блок
        v = self.vision_proj(vision)  # → (1, 32)
        d = self.dir_proj(direction)
        f = self.flags_proj(flags)
        c = self.coords_proj(coords)
        n = self.nearby_proj(nearby)
        cl = self.colony_proj(colony)

        # Конкатенация
        x = torch.cat([t, v, d, f, c, n, cl], dim=1).unsqueeze(1)  # (batch=1, seq=1, input_dim)

        # LSTM
        lstm_out, new_hidden = self.lstm(x, hidden_state)  # lstm_out: (1, 1, hidden)
        lstm_out = lstm_out[:, -1, :]  # убираем seq dim → (1, hidden)

        # Actor & Critic
        action_logits = self.actor(lstm_out)  # (1, num_actions)
        state_value = self.critic(lstm_out)   # (1, 1)

        return action_logits, state_value, new_hidden

    def init_hidden(self):
        return (
            torch.zeros(1, 1, self.lstm.hidden_size),
            torch.zeros(1, 1, self.lstm.hidden_size)
        )
