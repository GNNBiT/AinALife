import os

import torch

from core.agent import Ant
from models.ant_net import AntNet
from models.trainer import Trainer
from core.world import World
from core.tile_types import TileType
from utils import ant_actions

from core.map_generator import generate_map, load_config

EPSILON_START = 0.5
EPSILON_END = 0.01
EPSILON_DECAY = 0.99989
epsilon = EPSILON_START

actions = [
    "MOVE_FORWARD",
    "MOVE_BACKWARD",
    "TURN_LEFT",
    "TURN_RIGHT",
    "PICK_FOOD",
    "DROP_FOOD"
]

# === 1. Параметры ===
EPISODES = 300
SEED = 42  # или любой другой seed

config = load_config("configs/map_config.yaml")  # путь укажи правильный

# === 2. Модель и тренер ===
model = AntNet()

# 🔄 Загрузка модели, если файл существует
if os.path.exists("trained_ant_model.pth"):
    model.load_state_dict(torch.load("trained_ant_model.pth"))
    print("🔁 Загружена ранее обученная модель.")
else:
    print("🆕 Новая модель будет обучена с нуля.")

trainer = Trainer(model, lr=3e-4, gamma=0.7, use_critic=False)


for ep in range(EPISODES):
    # === 3. Генерация карты и муравья ===
    world, colony_centers = generate_map(config)

    cx, cy = colony_centers[0]  # первый муравейник
    ant = Ant(cx, cy, (cx, cy))

    ant.brain.model = model
    ants = [ant]
    episode_reward = 0

    while ant.is_alive():
        reward, inputs, decision = ant.act(world, ants, epsilon=epsilon)

        # И просто используй из "decision", который уже вернулся из think:
        action_name = decision["action"]
        logits = torch.tensor(decision["logits"]).unsqueeze(0)
        value = torch.tensor([[decision["value"]]], dtype=torch.float32)

        action_dist = torch.distributions.Categorical(logits=logits)
        action_idx = action_dist.sample().item()

        # ✅ Тут самое важное:
        trainer.record_step(
            inputs,
            action_idx,
            value.item(),
            float(reward),
            logits)

        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
        episode_reward += reward

    trainer.train_from_trajectory_n_step(n_steps=50)

    print(f"[EPISODE {ep}] steps: {ant.steps}, energy: {ant.energy:.2f}, reward: {episode_reward:.2f}")

import json
with open("debug_data.json", "w") as f:
    json.dump(trainer.debug_log, f)
print("📊 Debug data saved to debug_data.json")


# === Сохраняем модель после последнего эпизода ===
torch.save(model.state_dict(), "trained_ant_model.pth")
print("✅ Модель сохранена в файл trained_ant_model.pth")