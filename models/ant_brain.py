import random

from models.info_packet import InfoPacket
from models.ant_net import AntNet
import torch

class AntBrain:
    def __init__(self):
        self.model = AntNet()
        self.model.eval()
        self.device = torch.device("cuda")  # или cuda при необходимости
        self.model.to(self.device)

        self.hidden_state = self.model.init_hidden()  # LSTM state
        self.memory = []
        self.inputs = {}

    def receive(self, packet: InfoPacket):
        if packet.type == "food_gone":
            self.memory = [p for p in self.memory if not (p.type == "food" and p.data == packet.data)]
        elif packet.type == "carrying_food":
            self.memory.append(packet)
        else:
            self.memory.append(packet)

    def decay_memory(self):
        self.memory = [p for p in self.memory if not p.decay()]

    def think(self, inputs, epsilon=0.0):
        self.inputs = inputs

        # Подготовка входов (без памяти!)
        model_inputs = {
            "vision": inputs["vision"],
            "direction": inputs["direction"],
            "flags": inputs["flags"],
            "tile_under": inputs["tile_under"],
            "coords": inputs["coords"],
            "colony": inputs["colony"],
            "nearby": inputs["nearby_ants"]
        }

        # Прогон через модель
        with torch.no_grad():
            logits, value, new_hidden = self.model(model_inputs, self.hidden_state)
            self.hidden_state = new_hidden  # сохраняем новое состояние

        # Выбор действия
        actions = ["MOVE_FORWARD", "MOVE_BACKWARD", "TURN_LEFT", "TURN_RIGHT", "PICK_FOOD", "DROP_FOOD"]
        # 💥 Epsilon-greedy выбор
        if random.random() < epsilon:
            action_idx = random.randint(0, len(actions) - 1)
        else:
            action_idx = torch.argmax(logits, dim=1).item()

        return {
            "action": actions[action_idx],
            "value": value.item(),  # если нужно использовать
            "logits": logits.squeeze(0).tolist()  # если понадобится для обучения
        }

    def get_memory_vector(self):
        # Пока — просто one-hot по типам памяти (заглушка)
        # Можно сделать списком фиксированной длины
        types = ["food", "danger", "colony", "food_gone"]
        vec = [0] * len(types)

        for p in self.memory:
            if p.type in types:
                idx = types.index(p.type)
                vec[idx] = 1  # можно сделать больше, если хочешь суммировать

        return vec
